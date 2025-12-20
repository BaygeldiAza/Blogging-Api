import { api } from "./client";
import { ENDPOINTS } from "./endpoints";

export async function listCommentsByPost(postId) {
  const { data } = await api.get(ENDPOINTS.comments.listByPost(postId));
  return data;
}

// your UI calls: createComment({ post_id, content })
export async function createComment(payload) {
  const postId = payload?.post_id;
  const content = payload?.content;

  const { data } = await api.post(
    ENDPOINTS.comments.createByPost(postId),
    { content }
  );

  return data;
}
