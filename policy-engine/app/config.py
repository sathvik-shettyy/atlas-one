from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	postgres_db: str = "atlas_one"
	postgres_user: str = "atlas"
	postgres_password: str = "atlas_strong_password"
	atlas_jwt_secret: str = "replace-with-64-char-random-secret"
	atlas_jwt_algorithm: str = "HS256"
	atlas_access_token_minutes: int = 30
	atlas_refresh_token_days: int = 7
	atlas_default_mfa_mode: str = "required"
	atlas_otp_static_code: str = "123456"
	atlasone_admin_password: str = "AtlasOneAdmin123!"
	atlasone_dev_password: str = "AtlasOneDev123!"
	atlasone_guest_password: str = "AtlasOneGuest123!"

	model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

	@property
	def database_url(self) -> str:
		return (
			f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
			f"@postgres:5432/{self.postgres_db}"
		)


settings = Settings()