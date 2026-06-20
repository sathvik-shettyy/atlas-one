from sqlalchemy.orm import Session

from app.config import settings
from app.models import User
from app.security import hash_password


def ensure_seed_users(db: Session) -> None:
	defaults = [
		{
			"username": "admin",
			"password": "AtlasOneAdmin123!",
			"role": "admin",
			"mfa_mode": "required",
		},
		{
			"username": "developer",
			"password": "AtlasOneDev123!",
			"role": "developer",
			"mfa_mode": "optional",
		},
		{
			"username": "guest",
			"password": "AtlasOneGuest123!",
			"role": "guest",
			"mfa_mode": "disabled",
		},
	]

	for account in defaults:
		existing = db.query(User).filter(User.username == account["username"]).one_or_none()
		if existing:
			continue
		db.add(
			User(
				username=account["username"],
				password_hash=hash_password(account["password"]),
				role=account["role"],
				mfa_mode=account["mfa_mode"],
				is_active=True,
			)
		)

	db.commit()


def resolve_mfa_mode(mfa_mode: str | None) -> str:
	return (mfa_mode or settings.atlas_default_mfa_mode).lower()

