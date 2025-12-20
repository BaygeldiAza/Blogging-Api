import React from "react";

function normalizeErrorMessage(error) {
  if (!error) return null;

  const detail = error?.response?.data?.detail;

  if (typeof detail === "string") return detail;

  // FastAPI can sometimes return detail as an array of objects
  if (Array.isArray(detail)) {
    return detail
      .map((d) => (typeof d === "string" ? d : d?.msg || JSON.stringify(d)))
      .join("; ");
  }

  if (error?.message) return error.message;

  try {
    return JSON.stringify(error);
  } catch {
    return "Unknown error";
  }
}

export default function ErrorBox({ error, title = "Error" }) {
  const msg = normalizeErrorMessage(error);
  if (!msg) return null;

  return (
    <div className="card error">
      <strong>{title}:</strong>
      <div className="muted" style={{ marginTop: 6 }}>{msg}</div>
    </div>
  );
}
