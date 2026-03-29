import http from "./http";

export const employeesApi = {
  list(params) {
    return http.get("/api/employees/", { params });
  },
  create(payload) {
    return http.post("/api/employees/", payload);
  },
  update(id, payload) {
    return http.patch(`/api/employees/${id}/`, payload);
  },
};
