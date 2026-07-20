import { useLocation } from "react-router";
import { NavLink } from "react-router";

const ErrorPage = () => {
    const location = useLocation();

    return (
        <div className="error-page">
            <h1>404 - Page Not Found</h1>
            <p>The page {location.pathname} does not exist.</p>
            <NavLink to="/" className="error-page-link">
                Go back to Home
            </NavLink>
        </div>
    )
}

export default ErrorPage;