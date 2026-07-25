import { Link, useNavigate } from "react-router-dom";
import "./Header.css";

const Header = () => {
  const navigate = useNavigate();
  const username = sessionStorage.getItem("username");

  const handleLogout = async () => {
    try {
      await fetch("/djangoapp/logout", { method: "GET" });
    } finally {
      sessionStorage.clear();
      navigate("/login");
    }
  };

  return (
    <header className="site-header">
      <Link className="brand" to="/">
        Best Cars Dealerships
      </Link>

      <nav className="main-nav" aria-label="Primary navigation">
        <Link to="/">Home</Link>
        <a href="/about">About Us</a>
        <a href="/contact">Contact Us</a>
      </nav>

      <div className="account-nav">
        {username ? (
          <>
            <span className="current-user" data-testid="current-user">
              {username}
            </span>
            <button type="button" className="link-button" onClick={handleLogout}>
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link className="register-link" to="/register">
              Register
            </Link>
          </>
        )}
      </div>
    </header>
  );
};

export default Header;
