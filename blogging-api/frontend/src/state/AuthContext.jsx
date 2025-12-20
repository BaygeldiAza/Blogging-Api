import React, { createContext, useContext, useEffect, useMemo, useState } from "react";
import { setAuthToken } from "../api/client";
import authApi from "../api/auth";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem("access_token") || null);

  useEffect(() => {
    setAuthToken(token);
  }, [token]);

  const login = async ({ username, password }) => {
    const data = await authApi.login({ username, password }); // {access_token, token_type}
    localStorage.setItem("access_token", data.access_token);
    setToken(data.access_token);
    return data;
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    setToken(null);
    setAuthToken(null);
  };

  const value = useMemo(() => ({ token, setToken, login, logout }), [token]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside <AuthProvider>");
  return ctx;
}
