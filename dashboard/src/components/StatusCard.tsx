type StatusCardProps = {
	title: string;
	value: string;
	healthy?: boolean;
};

export default function StatusCard({ title, value, healthy = true }: StatusCardProps): JSX.Element {
	return (
		<article className="status-card">
			<header>{title}</header>
			<div className={`status-pill ${healthy ? "healthy" : "warning"}`}>{value}</div>
		</article>
	);
}

