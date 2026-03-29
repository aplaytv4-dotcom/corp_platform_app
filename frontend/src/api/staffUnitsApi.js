import http from "./http";

export const staffUnitsApi = {
  list(params) {
    return http.get("/api/staff-units/", { params });
  },
  create(payload) {
    return http.post("/api/staff-units/", payload);
  },
  update(id, payload) {
    return http.patch(`/api/staff-units/${id}/`, payload);
  },
};
