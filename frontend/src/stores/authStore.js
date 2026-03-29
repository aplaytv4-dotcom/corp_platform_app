import { defineStore } from "pinia";

import { authApi } from "@/api/authApi";
import router from "@/router";
import { storage } from "@/utils/storage";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    accessToken: storage.get("auth.tokens", {}).access || "",
    refreshTokenValue: storage.get("auth.tokens", {}).refresh || "",
    user: storage.get("auth.user", null),
    loading: false,
  }),
  getters: {
    role: (state) => state.user?.role || "",
    scopeType: (state) => state.user?.scope_type || "",
    allowedDepartments: (state) => {
      if (!state.user) return [];
      if (state.user.scope_type === "department" && state.user.department) {
        return [state.user.department];
      }
      return [];
    },
    isAuthenticated: (state) => Boolean(state.accessToken),
    isAdmin: (state) => state.user?.role === "admin",
    isManager: (state) => state.user?.role === "manager",
  },
  actions: {
    persistTokens(access, refresh) {
      this.accessToken = access;
      this.refreshTokenValue = refresh;
      storage.set("auth.tokens", { access, refresh });
    },
    setUser(user) {
      this.user = user;
      storage.set("auth.user", user);
    },
    canAccessDepartment(departmentId) {
      if (this.isAdmin || this.scopeType === "all") return true;
      if (this.scopeType === "department") {
        return Number(this.user?.department) === Number(departmentId) || Number(this.user?.department?.id) === Number(departmentId);
      }
      if (this.scopeType === "management") return true;
      return false;
    },
    async login(credentials) {
      this.loading = true;
      try {
        const { data } = await authApi.login(credentials);
        this.persistTokens(data.access, data.refresh);
        this.setUser(data.user);
        await this.fetchMe();
        await router.push("/attendance");
      } finally {
        this.loading = false;
      }
    },
    async fetchMe() {
      const { data } = await authApi.me();
      this.setUser(data);
      return data;
    },
    async refreshToken() {
      if (!this.refreshTokenValue) return null;
      const { data } = await authApi.refresh({ refresh: this.refreshTokenValue });
      this.persistTokens(data.access, data.refresh || this.refreshTokenValue);
      return data.access;
    },
    logout() {
      this.accessToken = "";
      this.refreshTokenValue = "";
      this.user = null;
      storage.remove("auth.tokens");
      storage.remove("auth.user");
      router.push("/login");
    },
  },
});
