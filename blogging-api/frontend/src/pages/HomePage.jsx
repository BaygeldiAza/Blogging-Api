import React, { useEffect, useState } from "react";
import * as postsApi from "../api/posts";
import Loading from "../components/Loading";
import ErrorBox from "../components/ErrorBox";
import PostList from "../components/PostList";

export default function HomePage() {
  const [posts, setPosts] = useState([]);
  const [busy, setBusy] = useState(true);
  const [err, setErr] = useState(null);

  const load = async () => {
    setErr(null);
    setBusy(true);
    try {
      const data = await postsApi.listPosts();
      const items = Array.isArray(data) ? data : (data?.items ?? []);
      setPosts(items);
    } catch (e) {
      setErr(e);
    } finally {
      setBusy(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <div className="container page">
      <div className="hero">
        <h1>Posts</h1>
        <button className="btn secondary" onClick={load} disabled={busy}>Refresh</button>
      </div>

      <ErrorBox error={err} />
      {busy ? <Loading /> : <PostList posts={posts} />}
    </div>
  );
}
