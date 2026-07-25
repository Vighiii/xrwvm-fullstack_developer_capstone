import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import Header from "../Header/Header";
import "./Login.css";

const Login = () => {
  const navigate = useNavigate();
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setSubmitting(true);

    try {
      const response = await fetch("/djangoapp/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userName, password }),
      });
      const data = await response.json();

      if (!response.ok || data.status !== "Authenticated") {
        throw new Error("The username or password is incorrect.");
      }

      sessionStorage.setItem("username", data.userName);
      sessionStorage.setItem("firstname", data.firstName || "");
      sessionStorage.setItem("lastname", data.lastName || "");
      navigate("/");
    } catch (requestError) {
      setError(requestError.message || "Login failed.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="page-shell">
      <Header />
      <main className="auth-page">
        <form className="auth-card" onSubmit={handleSubmit}>
          <h1>Welcome back</h1>
          <p>Sign in to review a dealership.</p>

          {error && <div className="auth-error">{error}</div>}

          <label htmlFor="username">Username</label>
          <input
            id="username"
            name="username"
            autoComplete="username"
            value={userName}
            onChange={(event) => setUserName(event.target.value)}
            required
          />

          <label htmlFor="password">Password</label>
          <input
            id="password"
            name="password"
            type="password"
            autoComplete="current-password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
          />

          <button type="submit" disabled={submitting}>
            {submitting ? "Signing in…" : "Login"}
          </button>

          <p className="auth-switch">
            New to Best Cars? <Link to="/register">Register now</Link>
          </p>
        </form>
      </main>
    </div>
  );
};

export default Login;
