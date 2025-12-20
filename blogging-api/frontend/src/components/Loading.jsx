import React from "react";

export default function Loading({ label = "Loading..." }) {
  return (
    <div className="card">
      <div className="muted">{label}</div>
    </div>
  );
}
