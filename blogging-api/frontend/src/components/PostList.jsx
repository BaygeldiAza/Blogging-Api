import React from "react";
import { Link } from "react-router-dom";

function truncate(text, max = 160) {
  if (!text) return "";
  return text.length > max ? text.slice(0, max) + "…" : text;
}

export default function PostList({ posts = [] }) {
  if (!posts.length) {
    return (
      <div className="card">
        <div className="muted">No posts yet.</div>
      </div>
    );
  }

  return (
    <div className="list">
      {posts.map((p) => {
        const author = p.author_username ?? p.author_id ?? "Unknown";
        const likes = p.likes_count ?? 0;
        const comments = p.comments_count ?? 0;

        return (
          <div className="card post-item" key={p.id}>
            <div className="post-head">
              <Link to={`/posts/${p.id}`} className="post-title">
                {p.title || "(Untitled)"}
              </Link>
              <div className="muted">by {author}</div>
            </div>

            <div className="post-body muted">{truncate(p.content)}</div>

            <div className="post-meta muted">
              ❤️ {likes} &nbsp;•&nbsp; 💬 {comments}
            </div>
          </div>
        );
      })}
    </div>
  );
}
