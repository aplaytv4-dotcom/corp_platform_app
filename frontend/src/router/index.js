import { createRouter, createWebHistory } from "vue-router";

import { routes } from "./routes";
import { useAuthStore } from "@/stores/authStore";

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to) => {
  const auth = useAuthStore();

  if (auth.accessToken && !auth.user) {
    try {
      await auth.fetchMe();
    } catch {
      auth.logout();
      return "/login";
    }
  }

  if (to.meta.guestOnly && auth.isAuthenticated) {
    return "/attendance";
  }

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return "/login";
  }

  if (to.meta.requiresAdmin && !auth.isAdmin) {
    return "/403";
  }

  return true;
});

export default router;
