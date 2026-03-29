import http from "./http";

export const usersApi = {
  list(params) {
    return http.get("/api/users/", { params });
  },
  create(payload) {
    return http.post("/api/users/", payload);
  },
  update(id, payload) {
    return http.patch(`/api/users/${id}/`, payload);
  },
};
