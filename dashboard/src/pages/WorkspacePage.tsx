import { useEffect } from "react";

export default function WorkspacePage() {
	useEffect(() => {
		window.location.assign("/workspace/");
	}, []);

	return (
		<main className="page page-login">
			<section className="glass-panel">
				<p className="eyebrow">ATLAS ONE WORKSPACE</p>
				<h1>Redirecting through Atlas One Gateway</h1>
			</section>
		</main>
	);
}

