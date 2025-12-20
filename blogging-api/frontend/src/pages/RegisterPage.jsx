import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import * as authApi from "../api/auth";
import ErrorBox from "../components/ErrorBox";

export default function RegisterPage() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState(null);
  const [ok, setOk] = useState(null);

  const onSubmit = async (e) => {
    e.preventDefault();
    setErr(null);
    setOk(null);
    setBusy(true);

    try {
      await authApi.register({ username, email, password });
      setOk("Registered successfully. Redirecting to login...");
      setTimeout(() => navigate("/login"), 700);
    } catch (e2) {
      setErr(e2);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="container page">
      <div className="card auth-card">
        <h2>Register</h2>

        <form onSubmit={onSubmit} className="form">
          <label>
            Username
            <input value={username} onChange={(e) => setUsername(e.target.value)} required />
          </label>

          <label>
            Email
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </label>

          <label>
            Password
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          </label>

          <button className="btn" disabled={busy}>
            {busy ? "Creating..." : "Create account"}
          </button>
        </form>

        {ok && <div className="card success">{ok}</div>}
        <ErrorBox error={err} />

        <div className="muted" style={{ marginTop: 10 }}>
          Already have an account? <Link to="/login">Login</Link>
        </div>
      </div>
    </div>
  );
}
