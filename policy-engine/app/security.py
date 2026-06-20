from passlib.context import CryptContext

from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
	return pwd_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
	return pwd_context.verify(plain_password, password_hash)


def is_mfa_verified(mfa_mode: str, otp: str | None) -> bool:
	mode = (mfa_mode or settings.atlas_default_mfa_mode).lower()

	if mode == "disabled":
		return True
	if mode == "optional":
		return otp in (None, "", settings.atlas_otp_static_code)
	return otp == settings.atlas_otp_static_code

