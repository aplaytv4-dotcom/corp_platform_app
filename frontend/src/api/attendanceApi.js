import http from "./http";

export const attendanceApi = {
  openOrCreate(payload) {
    return http.post("/api/attendance-sheets/open-or-create/", payload);
  },
  getById(id) {
    return http.get(`/api/attendance-sheets/${id}/`);
  },
  bulkUpdate(id, payload) {
    return http.patch(`/api/attendance-sheets/${id}/bulk-update/`, payload);
  },
};
