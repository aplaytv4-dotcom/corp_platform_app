import http from "./http";

export const absenceReasonsApi = {
  list(params) {
    return http.get("/api/absence-reasons/", { params });
  },
  create(payload) {
    return http.post("/api/absence-reasons/", payload);
  },
  update(id, payload) {
    return http.patch(`/api/absence-reasons/${id}/`, payload);
  },
};
