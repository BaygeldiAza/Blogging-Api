// src/api/client.js
import axios from "axios";

const baseURL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export const api = axios.create({
  baseURL,
});

export function setAuthToken(token) {
  if (token) {
    api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common["Authorization"];
  }
}

/**
 * Accepts only STRING urls. If you pass an object, you'll get your "replace is not a function".
 */
export function buildURL(relativeURL, params = {}) {
  if (typeof relativeURL !== "string") {
    throw new Error(
      `buildURL() expected a string but got: ${typeof relativeURL}. Check ENDPOINTS.`
    );
  }

  let url = relativeURL;

  // Replace {id} style params if you use them
  url = url.replace(/\{(\w+)\}/g, (_, key) => {
    if (params[key] === undefined) return `{${key}}`;
    return encodeURIComponent(params[key]);
  });

  return url;
}
