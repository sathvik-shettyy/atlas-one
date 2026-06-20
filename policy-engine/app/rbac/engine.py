ROLE_POLICIES = {
	"admin": {"workspace"},
	"developer": {"workspace"},
	"guest": {"workspace"},
}


def is_role_allowed(role: str, resource: str) -> bool:
	normalized_role = (role or "guest").lower()
	return resource in ROLE_POLICIES.get(normalized_role, set())


def policy_decision(
	*,
	is_active: bool,
	mfa_verified: bool,
	role: str,
	resource: str,
) -> tuple[bool, str]:
	if not is_active:
		return False, "User account is inactive"
	if not mfa_verified:
		return False, "MFA check failed"
	if not is_role_allowed(role, resource):
		return False, "Role is not allowed for requested resource"
	return True, "Access granted"

