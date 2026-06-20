from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
	username: str = Field(min_length=3, max_length=100)
	password: str = Field(min_length=8, max_length=128)
	otp: str | None = Field(default=None, min_length=6, max_length=6)


class SessionResponse(BaseModel):
	authenticated: bool
	username: str | None = None
	role: str | None = None
	mfa_mode: str | None = None


class PolicyResult(BaseModel):
	allowed: bool
	reason: str


class PasswordResetRequest(BaseModel):
	username: str


class PasswordResetConfirm(BaseModel):
	token: str
	new_password: str = Field(min_length=8, max_length=128)

