import React, { useState } from "react";
import { useAuth } from "../state/AuthContext";
import * as likesApi from "../api/likes";
import ErrorBox from "./ErrorBox";

export default function LikeButton({ postId, initialCount = 0, initialLiked = false, onChange }) {
  const { token } = useAuth();
  const [liked, setLiked] = useState(Boolean(initialLiked));
  const [count, setCount] = useState(Number(initialCount) || 0);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState(null);

  const toggle = async () => {
    setErr(null);

    if (!token) {
      setErr(new Error("Please log in to like posts."));
      return;
    }

    if (busy) return;
    setBusy(true);

    try {
      if (liked) {
        await likesApi.unlikePost(postId);
        setLiked(false);
        setCount((c) => Math.max(0, c - 1));
        onChange?.({ liked: false, count: Math.max(0, count - 1) });
      } else {
        await likesApi.likePost(postId);
        setLiked(true);
        setCount((c) => c + 1);
        onChange?.({ liked: true, count: count + 1 });
      }
    } catch (e) {
      setErr(e);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div>
      <button className="btn" disabled={busy} onClick={toggle}>
        {liked ? "Unlike" : "Like"} ({count})
      </button>
      <ErrorBox error={err} />
    </div>
  );
}
