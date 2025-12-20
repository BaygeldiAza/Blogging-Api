import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../state/AuthContext";
import ErrorBox from "../components/ErrorBox";

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState(null);

  const onSubmit = async (e) => {
    e.preventDefault();
    setErr(null);
    setBusy(true);

    try {
      // ✅ FIX: AuthContext.login expects an object { username, password }
      await login({ username, password });
      navigate("/");
    } catch (e2) {
      setErr(e2);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="container page">
      <div className="card auth-card">
        <h2>Login</h2>
        <p className="muted">
          Use your email
        </p>

        <form onSubmit={onSubmit} className="form">
          <label>
            Email
            <input value={username} onChange={(e) => setUsername(e.target.value)} required />
          </label>

          <label>
            Password
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          </label>

          <button className="btn" disabled={busy}>
            {busy ? "Logging in..." : "Login"}
          </button>
        </form>

        <ErrorBox error={err} />

        <div className="muted" style={{ marginTop: 10 }}>
          No account? <Link to="/register">Register</Link>
        </div>
      </div>
    </div>
  );
}
