import { useState } from "react";
import { loginUser } from "../services/api";

const Login = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading]     = useState(false);
  const [error, setError]         = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!username.trim() || !password.trim()) {
      setError("Please enter both username and password.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const res = await loginUser(username.trim(), password);
      if (res && res.data && res.data.user) {
        onLoginSuccess(res.data.user);
      } else {
        setError("Login response missing user profile.");
      }
    } catch (err) {
      const msg =
        err?.response?.data?.message ||
        err?.response?.data?.errors?.[0]?.message ||
        "Invalid username or password. Please verify and try again.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-wrapper">
      <div className="login-card">
        {/* Brand Header */}
        <div className="login-brand">
          <img
            src="/node-solutions-logo.svg"
            alt="Node Solutions"
            className="login-logo"
          />
          <h1 className="login-title">AI Request Triage</h1>
          <p className="login-subtitle">
            Sign in to access the enterprise classification system
          </p>
        </div>

        {/* Error Notification */}
        {error && (
          <div className="login-error-alert" role="alert">
            <svg
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="8" x2="12" y2="12" />
              <line x1="12" y1="16" x2="12.01" y2="16" />
            </svg>
            <span>{error}</span>
          </div>
        )}

        {/* Login Form */}
        <form className="login-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="login-username">Username</label>
            <input
              id="login-username"
              type="text"
              placeholder="Enter username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              disabled={loading}
              autoComplete="username"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="login-password">Password</label>
            <input
              id="login-password"
              type="password"
              placeholder="••••••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={loading}
              autoComplete="current-password"
              required
            />
          </div>

          <button
            type="submit"
            className="login-submit-btn"
            disabled={loading}
          >
            {loading ? (
              <span className="btn-spinner-label">
                <span className="spinner-inline" /> Verifying Credentials...
              </span>
            ) : (
              "Sign In to Dashboard"
            )}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;
