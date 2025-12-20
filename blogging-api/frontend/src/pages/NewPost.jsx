import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createPost } from "../api/posts.js";

export default function NewPost() {
  const navigate = useNavigate();

  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [err, setErr] = useState("");
  const [loading, setLoading] = useState(false);

  async function onSubmit(e) {
    e.preventDefault();
    setErr("");

    if (!title.trim() || !content.trim()) {
      setErr("Title and content are required.");
      return;
    }

    setLoading(true);
    try {
      const created = await createPost({ title: title.trim(), content: content.trim() });
      navigate(`/posts/${created.id}`);
    } catch (e2) {
      setErr(e2?.response?.data?.detail || "Failed to create post.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="container">
      <div className="row">
        <h2>New Post</h2>
        <button className="btn" onClick={() => navigate(-1)}>Back</button>
      </div>

      <div className="card">
        <form className="stack" onSubmit={onSubmit}>
          <div>
            <label className="muted">Title</label>
            <input
              className="input"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Post title"
            />
          </div>

          <div>
            <label className="muted">Content</label>
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="Write your post..."
            />
          </div>

          {err && <div className="error">{err}</div>}

          <button className="btn primary" disabled={loading}>
            {loading ? "Creating..." : "Create Post"}
          </button>
        </form>
      </div>
    </div>
  );
}
