import { api } from "./client";
import { ENDPOINTS } from "./endpoints";

export async function listPosts() {
  const { data } = await api.get(ENDPOINTS.posts.list);
  return data;
}

export async function getPost(id) {
  const { data } = await api.get(ENDPOINTS.posts.detail(id));
  return data;
}

export async function createPost(payload) {
  const { data } = await api.post(ENDPOINTS.posts.create, payload);
  return data;
}
