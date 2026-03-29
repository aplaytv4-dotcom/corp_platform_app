import axios from "axios";

import { storage } from "@/utils/storage";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const http = axios.create({
  baseURL: API_BASE_URL,
});

let refreshingPromise = null;

function getTokens() {
  return storage.get("auth.tokens", {
    access: "",
    refresh: "",
  });
}

function setTokens(tokens) {
  storage.set("auth.tokens", tokens);
}

function clearTokens() {
  storage.remove("auth.tokens");
  storage.remove("auth.user");
}

http.interceptors.request.use((config) => {
  const tokens = getTokens();
  if (tokens?.access) {
    config.headers.Authorization = `Bearer ${tokens.access}`;
  }
  return config;
});

http.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    const tokens = getTokens();

    if (
      error.response?.status === 401 &&
      !originalRequest?._retry &&
      tokens?.refresh &&
      !String(originalRequest?.url || "").includes("/api/auth/login/") &&
      !String(originalRequest?.url || "").includes("/api/auth/refresh/")
    ) {
      originalRequest._retry = true;

      if (!refreshingPromise) {
        refreshingPromise = axios
          .post(`${API_BASE_URL}/api/auth/refresh/`, { refresh: tokens.refresh })
          .then((response) => {
            const nextTokens = {
              access: response.data.access,
              refresh: response.data.refresh || tokens.refresh,
            };
            setTokens(nextTokens);
            return nextTokens;
          })
          .catch((refreshError) => {
            clearTokens();
            throw refreshError;
          })
          .finally(() => {
            refreshingPromise = null;
          });
      }

      const nextTokens = await refreshingPromise;
      originalRequest.headers.Authorization = `Bearer ${nextTokens.access}`;
      return http(originalRequest);
    }

    return Promise.reject(error);
  },
);

export default http;
