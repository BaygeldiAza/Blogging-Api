import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import * as postsApi from "../api/posts";
import ErrorBox from "../components/ErrorBox";

export default function NewPostPage() {
  const navigate = useNavigate();

  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState(null);

  const onSubmit = async (e) => {
    e.preventDefault();
    setErr(null);
    setBusy(true);

    try {
      const created = await postsApi.createPost({ title, content });
      if (!created?.id) throw new Error("Post created but no id returned.");
      navigate(`/posts/${created.id}`);
    } catch (e2) {
      setErr(e2);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="container page">
      <div className="card">
        <h2>New Post</h2>

        <form onSubmit={onSubmit} className="form">
          <label>
            Title
            <input value={title} onChange={(e) => setTitle(e.target.value)} required />
          </label>

          <label>
            Content
            <textarea rows={8} value={content} onChange={(e) => setContent(e.target.value)} required />
          </label>

          <button className="btn" disabled={busy}>
            {busy ? "Publishing..." : "Publish"}
          </button>
        </form>

        <ErrorBox error={err} />
      </div>
    </div>
  );
}
