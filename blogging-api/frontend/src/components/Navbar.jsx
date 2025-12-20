import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../state/AuthContext";

export default function Navbar() {
  const { token, logout } = useAuth();
  const navigate = useNavigate();

  const onLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <div className="nav">
      <div className="nav-inner container">
        <Link to="/" className="brand">Blog</Link>

        <div className="nav-links">
          {token ? (
            <>
              <Link to="/new" className="btn">New Post</Link>
              <button className="btn secondary" onClick={onLogout}>Logout</button>
            </>
          ) : (
            <>
              <Link to="/login" className="btn">Login</Link>
              <Link to="/register" className="btn secondary">Register</Link>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
