import http from "./http";

export const authApi = {
  login(payload) {
    return http.post("/api/auth/login/", payload);
  },
  refresh(payload) {
    return http.post("/api/auth/refresh/", payload);
  },
  me() {
    return http.get("/api/auth/me/");
  },
  changePassword(payload) {
    return http.post("/api/auth/change-password/", payload);
  },
};
