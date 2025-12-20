// src/api/endpoints.js
export const ENDPOINTS = {
  users: {
    register: "/users/register",
    login: "/users/login",
    me: "/users/me",
  },
  posts: {
    list: "/posts/",
    detail: (id) => `/posts/${id}`,
    create: "/posts/",
  },
  comments: {
    listByPost: (postId) => `/posts/${postId}/comments`,
    createByPost: (postId) => `/posts/${postId}/comments`,
  },
  likes: {
    likePost: "/likes/",
    unlikePost: (postId) => `/likes/${postId}`,
  },
};
