import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import StatusCard from "../components/StatusCard";

type Session = {
	authenticated: boolean;
	username?: string;
	role?: string;
};

export default function DashboardPage() {
	const navigate = useNavigate();
	const [session, setSession] = useState<Session>({ authenticated: false });

	useEffect(() => {
		const loadSession = async () => {
			const response = await fetch("/api/auth/session", {
				credentials: "include"
			});
			if (!response.ok) {
				navigate("/login");
				return;
			}
			const payload = (await response.json()) as Session;
			if (!payload.authenticated) {
				navigate("/login");
				return;
			}
			setSession(payload);
		};

		void loadSession();
	}, [navigate]);

	const logout = async () => {
		await fetch("/api/auth/logout", { method: "POST", credentials: "include" });
		navigate("/login");
	};

	return (
		<main className="page">
			<header className="top-bar">
				<div>
					<p className="eyebrow">ATLAS ONE</p>
					<h1>Zero Trust Secure Access Platform</h1>
				</div>
				<button onClick={logout} className="ghost-button">
					Logout
				</button>
			</header>

			<section className="status-grid">
				<StatusCard title="Gateway" value="Online" />
				<StatusCard title="Identity" value="Online" />
				<StatusCard title="MFA" value="Enabled" />
				<StatusCard title="Policy Engine" value="Running" />
			</section>

			<section className="panel">
				<h2>Applications</h2>
				<div className="app-item">
					<div>
						<h3>Workspace</h3>
						<p>Protected by Atlas One Gateway and Policy Engine.</p>
					</div>
					<Link className="primary-link" to="/workspace">
						Open Workspace
					</Link>
				</div>
			</section>

			<section className="meta-grid">
				<article className="panel">
					<h3>Role</h3>
					<p>{session.role ?? "Administrator"}</p>
				</article>
				<article className="panel">
					<h3>Session</h3>
					<p>{session.authenticated ? "Active" : "Inactive"}</p>
				</article>
				<article className="panel">
					<h3>User</h3>
					<p>{session.username ?? "Unknown"}</p>
				</article>
			</section>
		</main>
	);
}

