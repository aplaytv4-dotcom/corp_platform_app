import http from "./http";

export const managementsApi = {
  list(params) {
    return http.get("/api/managements/", { params });
  },
  create(payload) {
    return http.post("/api/managements/", payload);
  },
  update(id, payload) {
    return http.patch(`/api/managements/${id}/`, payload);
  },
};
