import { FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function LoginPage(): JSX.Element {
	const navigate = useNavigate();
	const [username, setUsername] = useState("admin");
	const [password, setPassword] = useState("AtlasOneAdmin123!");
	const [otp, setOtp] = useState("123456");
	const [error, setError] = useState<string | null>(null);
	const [isSubmitting, setIsSubmitting] = useState(false);

	const onSubmit = async (event: FormEvent) => {
		event.preventDefault();
		setIsSubmitting(true);
		setError(null);

		const response = await fetch("/api/auth/login", {
			method: "POST",
			credentials: "include",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ username, password, otp })
		});

		if (!response.ok) {
			setError("Authentication failed. Check credentials and OTP.");
			setIsSubmitting(false);
			return;
		}

		navigate("/");
	};

	return (
		<main className="page page-login">
			<section className="glass-panel">
				<p className="eyebrow">ATLAS ONE GATEWAY</p>
				<h1>Atlas One Login</h1>
				<p>Secure access requires identity verification and policy checks.</p>
				<form onSubmit={onSubmit} className="atlas-form">
					<label>
						Username
						<input value={username} onChange={(e) => setUsername(e.target.value)} required />
					</label>
					<label>
						Password
						<input
							type="password"
							value={password}
							onChange={(e) => setPassword(e.target.value)}
							required
						/>
					</label>
					<label>
						One-Time Passcode
						<input value={otp} onChange={(e) => setOtp(e.target.value)} maxLength={6} />
					</label>
					{error ? <div className="error-text">{error}</div> : null}
					<button type="submit" disabled={isSubmitting}>
						{isSubmitting ? "Authenticating..." : "Access Atlas One"}
					</button>
				</form>
			</section>
		</main>
	);
}

