import secrets

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.jwt.tokens import create_access_token, create_refresh_token, decode_token
from app.models import PasswordResetToken, User
from app.rbac.engine import policy_decision
from app.schemas import (
	LoginRequest,
	PasswordResetConfirm,
	PasswordResetRequest,
	PolicyResult,
	SessionResponse,
)
from app.security import hash_password, is_mfa_verified, verify_password
from app.seed import ensure_seed_users, resolve_mfa_mode

app = FastAPI(title="Atlas One Policy Engine", version="0.1.0")

app.add_middleware(
	CORSMiddleware,
	allow_origins=["http://localhost:8080"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


def _set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
	response.set_cookie(
		key="atlas_access_token",
		value=access_token,
		httponly=True,
		secure=False,
		samesite="lax",
		max_age=60 * 30,
		path="/",
	)
	response.set_cookie(
		key="atlas_refresh_token",
		value=refresh_token,
		httponly=True,
		secure=False,
		samesite="lax",
		max_age=60 * 60 * 24 * 7,
		path="/",
	)


def _clear_auth_cookies(response: Response) -> None:
	response.delete_cookie("atlas_access_token", path="/")
	response.delete_cookie("atlas_refresh_token", path="/")


def _decode_access_from_request(request: Request) -> dict:
	token = request.cookies.get("atlas_access_token")
	if not token:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
	payload = decode_token(token)
	if not payload or payload.get("type") != "access":
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session token")
	return payload


@app.on_event("startup")
def startup() -> None:
	Base.metadata.create_all(bind=engine)
	with Session(engine) as db:
		ensure_seed_users(db)


@app.get("/health")
def health() -> dict[str, str]:
	return {"status": "ok", "service": "atlas-policy-engine"}


@app.post("/auth/login")
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)) -> dict[str, str]:
	user = db.query(User).filter(User.username == payload.username).one_or_none()
	if not user or not verify_password(payload.password, user.password_hash):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

	mfa_mode = resolve_mfa_mode(user.mfa_mode)
	if not is_mfa_verified(mfa_mode, payload.otp):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid MFA verification")

	access_token = create_access_token(
		subject=user.username,
		role=user.role,
		mfa_verified=True,
	)
	refresh_token = create_refresh_token(subject=user.username)
	_set_auth_cookies(response, access_token, refresh_token)

	return {"message": "Login successful"}


@app.post("/auth/logout")
def logout(response: Response) -> dict[str, str]:
	_clear_auth_cookies(response)
	return {"message": "Logged out"}


@app.post("/auth/refresh")
def refresh(response: Response, request: Request, db: Session = Depends(get_db)) -> dict[str, str]:
	refresh_token = request.cookies.get("atlas_refresh_token")
	if not refresh_token:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing refresh token")

	payload = decode_token(refresh_token)
	if not payload or payload.get("type") != "refresh":
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

	username = payload.get("sub")
	user = db.query(User).filter(User.username == username).one_or_none()
	if not user:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

	access_token = create_access_token(subject=user.username, role=user.role, mfa_verified=True)
	new_refresh_token = create_refresh_token(subject=user.username)
	_set_auth_cookies(response, access_token, new_refresh_token)
	return {"message": "Session refreshed"}


@app.get("/auth/session", response_model=SessionResponse)
def session_status(request: Request, db: Session = Depends(get_db)) -> SessionResponse:
	token = request.cookies.get("atlas_access_token")
	if not token:
		return SessionResponse(authenticated=False)

	payload = decode_token(token)
	if not payload or payload.get("type") != "access":
		return SessionResponse(authenticated=False)

	user = db.query(User).filter(User.username == payload.get("sub")).one_or_none()
	if not user:
		return SessionResponse(authenticated=False)

	return SessionResponse(
		authenticated=True,
		username=user.username,
		role=user.role,
		mfa_mode=resolve_mfa_mode(user.mfa_mode),
	)


@app.post("/policy/evaluate", response_model=PolicyResult)
def evaluate_policy(request: Request, resource: str = "workspace", db: Session = Depends(get_db)) -> PolicyResult:
	payload = _decode_access_from_request(request)
	user = db.query(User).filter(User.username == payload.get("sub")).one_or_none()
	if not user:
		return PolicyResult(allowed=False, reason="User not found")

	allowed, reason = policy_decision(
		is_active=user.is_active,
		mfa_verified=bool(payload.get("mfa_verified", False)),
		role=user.role,
		resource=resource,
	)
	return PolicyResult(allowed=allowed, reason=reason)


@app.get("/gateway/authorize")
def gateway_authorize(request: Request, db: Session = Depends(get_db)) -> Response:
	payload = _decode_access_from_request(request)
	user = db.query(User).filter(User.username == payload.get("sub")).one_or_none()
	if not user:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User missing")

	allowed, reason = policy_decision(
		is_active=user.is_active,
		mfa_verified=bool(payload.get("mfa_verified", False)),
		role=user.role,
		resource="workspace",
	)
	if not allowed:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=reason)

	return Response(status_code=status.HTTP_200_OK)


@app.post("/auth/password-reset/request")
def password_reset_request(payload: PasswordResetRequest, db: Session = Depends(get_db)) -> dict[str, str]:
	user = db.query(User).filter(User.username == payload.username).one_or_none()
	if not user:
		return {"message": "If the account exists, a reset token has been issued"}

	token = f"atlas-reset-{secrets.token_urlsafe(16)}"
	db.add(PasswordResetToken(username=user.username, token=token, is_used=False))
	db.commit()
	return {"message": "Reset token generated for demo", "token": token}


@app.post("/auth/password-reset/confirm")
def password_reset_confirm(payload: PasswordResetConfirm, db: Session = Depends(get_db)) -> dict[str, str]:
	reset = db.query(PasswordResetToken).filter(PasswordResetToken.token == payload.token).one_or_none()
	if not reset or reset.is_used:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid reset token")

	user = db.query(User).filter(User.username == reset.username).one_or_none()
	if not user:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

	user.password_hash = hash_password(payload.new_password)
	reset.is_used = True
	db.commit()
	return {"message": "Password updated"}


@app.get("/auth/sso/start")
def sso_start() -> dict[str, str]:
	return {"message": "SSO bootstrap ready via Atlas One Identity Engine"}


@app.get("/auth/sso/callback")
def sso_callback() -> dict[str, str]:
	return {"message": "SSO callback received"}

