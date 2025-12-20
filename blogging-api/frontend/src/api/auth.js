// src/api/auth.js
import { api } from "./client";
import { ENDPOINTS } from "./endpoints";

export async function register(payload) {
  const res = await api.post(ENDPOINTS.users.register, payload);
  return res.data;
}

// Your backend uses OAuth2PasswordRequestForm -> x-www-form-urlencoded
export async function login({ username, password }) {
  const body = new URLSearchParams();
  body.append("username", username);
  body.append("password", password);

  const res = await api.post(ENDPOINTS.users.login, body, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });

  return res.data; // {access_token, token_type}
}

export async function me() {
  const res = await api.get(ENDPOINTS.users.me);
  return res.data;
}

// ✅ default export (so authApi.login works)
const authApi = { register, login, me };
export default authApi;
