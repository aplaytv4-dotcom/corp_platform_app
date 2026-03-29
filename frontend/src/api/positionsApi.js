import http from "./http";

export const positionsApi = {
  list(params) {
    return http.get("/api/positions/", { params });
  },
  create(payload) {
    return http.post("/api/positions/", payload);
  },
  update(id, payload) {
    return http.patch(`/api/positions/${id}/`, payload);
  },
};
