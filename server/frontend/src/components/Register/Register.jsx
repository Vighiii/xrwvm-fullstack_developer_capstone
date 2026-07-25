import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import "../Login/Login.css";
import "./Register.css";

const Register = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    userName: "",
    firstName: "",
    lastName: "",
    email: "",
    password: "",
  });
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const updateField = (event) => {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setSubmitting(true);

    try {
      const response = await fetch("/djangoapp/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const data = await response.json();

      if (!response.ok || data.status !== "Authenticated") {
        throw new Error(data.message || "This username is already registered.");
      }

      sessionStorage.setItem("username", data.userName);
      sessionStorage.setItem("firstname", data.firstName || form.firstName);
      sessionStorage.setItem("lastname", data.lastName || form.lastName);
      navigate("/");
    } catch (requestError) {
      setError(requestError.message || "Registration failed.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <main className="auth-page register-page">
      <form className="auth-card register-card" onSubmit={handleSubmit}>
        <div className="register-heading">
          <div>
            <h1>Sign Up</h1>
            <p>Create your Best Cars account.</p>
          </div>
          <Link className="close-link" to="/" aria-label="Close registration">
            ×
          </Link>
        </div>

        {error && <div className="auth-error">{error}</div>}

        <label htmlFor="register-username">Username</label>
        <input
          id="register-username"
          type="text"
          name="userName"
          placeholder="Username"
          value={form.userName}
          onChange={updateField}
          required
        />

        <label htmlFor="register-firstname">First Name</label>
        <input
          id="register-firstname"
          type="text"
          name="firstName"
          placeholder="First Name"
          value={form.firstName}
          onChange={updateField}
          required
        />

        <label htmlFor="register-lastname">Last Name</label>
        <input
          id="register-lastname"
          type="text"
          name="lastName"
          placeholder="Last Name"
          value={form.lastName}
          onChange={updateField}
          required
        />

        <label htmlFor="register-email">Email</label>
        <input
          id="register-email"
          type="email"
          name="email"
          placeholder="Email"
          value={form.email}
          onChange={updateField}
          required
        />

        <label htmlFor="register-password">Password</label>
        <input
          id="register-password"
          type="password"
          name="password"
          placeholder="Password"
          value={form.password}
          onChange={updateField}
          minLength="8"
          required
        />

        <button type="submit" disabled={submitting}>
          {submitting ? "Creating account…" : "Register"}
        </button>
      </form>
    </main>
  );
};

export default Register;
