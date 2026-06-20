from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.config import settings


def create_access_token(subject: str, role: str, mfa_verified: bool) -> str:
	now = datetime.now(tz=timezone.utc)
	payload = {
		"sub": subject,
		"role": role,
		"mfa_verified": mfa_verified,
		"type": "access",
		"iat": int(now.timestamp()),
		"exp": int((now + timedelta(minutes=settings.atlas_access_token_minutes)).timestamp()),
	}
	return jwt.encode(payload, settings.atlas_jwt_secret, algorithm=settings.atlas_jwt_algorithm)


def create_refresh_token(subject: str) -> str:
	now = datetime.now(tz=timezone.utc)
	payload = {
		"sub": subject,
		"type": "refresh",
		"iat": int(now.timestamp()),
		"exp": int((now + timedelta(days=settings.atlas_refresh_token_days)).timestamp()),
	}
	return jwt.encode(payload, settings.atlas_jwt_secret, algorithm=settings.atlas_jwt_algorithm)


def decode_token(token: str) -> dict | None:
	try:
		return jwt.decode(token, settings.atlas_jwt_secret, algorithms=[settings.atlas_jwt_algorithm])
	except JWTError:
		return None

