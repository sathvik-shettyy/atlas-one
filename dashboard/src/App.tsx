import { Navigate, Route, Routes } from "react-router-dom";
import DashboardPage from "./pages/DashboardPage";
import LoginPage from "./pages/LoginPage";
import WorkspacePage from "./pages/WorkspacePage";

export default function App(): JSX.Element {
	return (
		<Routes>
			<Route path="/login" element={<LoginPage />} />
			<Route path="/workspace" element={<WorkspacePage />} />
			<Route path="/" element={<DashboardPage />} />
			<Route path="*" element={<Navigate to="/" replace />} />
		</Routes>
	);
}

