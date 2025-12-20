import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { login } from "../api/auth.js";
import { useAuth } from "../context/AuthContext.jsx";

export default function Login() {
  const navigate = useNavigate();
  const { setToken } = useAuth();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [err, setErr] = useState("");
  const [loading, setLoading] = useState(false);

  async function onSubmit(e) {
    e.preventDefault();
    setErr("");
    setLoading(true);
    try {
      const data = await login(username, password);
      setToken(data.access_token);
      navigate("/posts");
    } catch (e2) {
      setErr(e2?.response?.data?.detail || "Login failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="container">
      <h2>Login</h2>

      <div className="card">
        <form className="stack" onSubmit={onSubmit}>
          <div>
            <label className="muted">Email (or email)</label>
            <input
              className="input"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="username"
              autoComplete="username"
            />
          </div>

          <div>
            <label className="muted">Password</label>
            <input
              className="input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="password"
              type="password"
              autoComplete="current-password"
            />
          </div>

          {err && <div className="error">{err}</div>}

          <button className="btn primary" disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </button>

          <div className="muted">
            No account? <Link to="/register">Register</Link>
          </div>
        </form>
      </div>
    </div>
  );
}
