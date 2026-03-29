import http from "./http";

export const assignmentsApi = {
  list(params) {
    return http.get("/api/assignments/", { params });
  },
  create(payload) {
    return http.post("/api/assignments/", payload);
  },
  close(id, payload) {
    return http.patch(`/api/assignments/${id}/close/`, payload);
  },
  transfer(payload) {
    return http.post("/api/assignments/transfer/", payload);
  },
};
