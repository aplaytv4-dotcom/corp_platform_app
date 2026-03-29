import http from "./http";

export const departmentsApi = {
  list(params) {
    return http.get("/api/departments/", { params });
  },
  create(payload) {
    return http.post("/api/departments/", payload);
  },
  update(id, payload) {
    return http.patch(`/api/departments/${id}/`, payload);
  },
};
