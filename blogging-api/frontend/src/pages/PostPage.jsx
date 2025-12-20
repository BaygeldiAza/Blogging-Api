import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import * as postsApi from "../api/posts";
import * as commentsApi from "../api/comments";
import { useAuth } from "../state/AuthContext";
import Loading from "../components/Loading";
import ErrorBox from "../components/ErrorBox";
import LikeButton from "../components/LikeButton";

export default function PostPage() {
  const { id } = useParams();
  const postId = Number(id);
  const { token } = useAuth();

  const [post, setPost] = useState(null);
  const [comments, setComments] = useState([]);

  const [busy, setBusy] = useState(true);
  const [err, setErr] = useState(null);

  const [commentText, setCommentText] = useState("");
  const [commentBusy, setCommentBusy] = useState(false);
  const [commentErr, setCommentErr] = useState(null);

  const load = async () => {
    setErr(null);
    setBusy(true);
    try {
      const p = await postsApi.getPost(postId);
      setPost(p);

      const c = await commentsApi.listCommentsByPost(postId);
      setComments(Array.isArray(c) ? c : (c?.items ?? []));
    } catch (e) {
      setErr(e);
    } finally {
      setBusy(false);
    }
  };

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [postId]);

  const submitComment = async (e) => {
    e.preventDefault();
    setCommentErr(null);

    if (!token) {
      setCommentErr(new Error("Please log in to comment."));
      return;
    }

    if (!commentText.trim()) return;

    setCommentBusy(true);
    try {
      await commentsApi.createComment({ post_id: postId, content: commentText.trim() });
      setCommentText("");
      const c = await commentsApi.listCommentsByPost(postId);
      setComments(Array.isArray(c) ? c : (c?.items ?? []));
    } catch (e2) {
      setCommentErr(e2);
    } finally {
      setCommentBusy(false);
    }
  };

  if (busy) return <div className="container page"><Loading /></div>;

  return (
    <div className="container page">
      <ErrorBox error={err} />
      {!post ? (
        <div className="card">
          <div className="muted">Post not found.</div>
        </div>
      ) : (
        <>
          <div className="card">
            <h2 style={{ marginTop: 0 }}>{post.title || "(Untitled)"}</h2>
            <div className="muted" style={{ marginBottom: 14 }}>
              by {post.author_username ?? post.author_id ?? "Unknown"}
            </div>

            <div className="content">{post.content}</div>

            <div style={{ marginTop: 16 }}>
              <LikeButton
                postId={postId}
                initialCount={post.likes_count ?? 0}
                initialLiked={post.liked_by_me ?? false}
              />
            </div>
          </div>

          <div className="card">
            <h3>Comments</h3>

            <div className="comments">
              {comments.length ? (
                comments.map((c) => (
                  <div key={c.id ?? `${c.author_id}-${c.created_at}-${c.content}`} className="comment">
                    <div className="muted">
                      {c.author_username ?? c.author_id ?? "Anon"}
                    </div>
                    <div>{c.content}</div>
                  </div>
                ))
              ) : (
                <div className="muted">No comments yet.</div>
              )}
            </div>

            <form onSubmit={submitComment} className="form" style={{ marginTop: 14 }}>
              <label>
                Add a comment
                <textarea
                  rows={3}
                  value={commentText}
                  onChange={(e) => setCommentText(e.target.value)}
                  placeholder={token ? "Write your comment..." : "Log in to comment"}
                  disabled={!token || commentBusy}
                />
              </label>

              <button className="btn" disabled={!token || commentBusy}>
                {commentBusy ? "Posting..." : "Post comment"}
              </button>
            </form>

            <ErrorBox error={commentErr} />
          </div>
        </>
      )}
    </div>
  );
}
