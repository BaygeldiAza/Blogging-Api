import { api } from "./client";
import { ENDPOINTS } from "./endpoints";

export async function likePost(postId) {
  const { data } = await api.post(ENDPOINTS.likes.likePost, { post_id: postId });
  return data;
}

export async function unlikePost(postId) {
  const { data } = await api.delete(ENDPOINTS.likes.unlikePost(postId));
  return data;
}
