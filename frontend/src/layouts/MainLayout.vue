<template>
  <div class="main-layout">
    <aside class="sidebar">
      <div class="brand">{{ t("appName") }}</div>
      <nav class="nav-list">
        <RouterLink v-for="item in menuItems" :key="item.to" :to="item.to" class="nav-link">
          {{ item.label }}
        </RouterLink>
      </nav>
    </aside>
    <div class="content">
      <header class="topbar">
        <LanguageSwitcher :model-value="ui.currentLanguage" @update:model-value="ui.setLanguage" />
        <div class="user-box">
          <div>
            <strong>{{ auth.user?.full_name || auth.user?.username }}</strong>
            <div class="muted">{{ auth.user?.role }}</div>
          </div>
          <div class="toolbar-row">
            <RouterLink to="/profile">{{ t("menu.profile") }}</RouterLink>
            <AppButton variant="secondary" @click="auth.logout">{{ t("actions.logout") }}</AppButton>
          </div>
        </div>
      </header>
      <main class="main-content">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { RouterLink } from "vue-router";
import { useI18n } from "vue-i18n";

import AppButton from "@/components/AppButton.vue";
import LanguageSwitcher from "@/components/LanguageSwitcher.vue";
import { useAuthStore } from "@/stores/authStore";
import { useUiStore } from "@/stores/uiStore";
import { buildMenu } from "@/utils/menu";

const auth = useAuthStore();
const ui = useUiStore();
const { t } = useI18n();

const menuItems = computed(() => buildMenu({ t, isAdmin: auth.isAdmin }));
</script>

<style scoped>
.main-layout {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 260px 1fr;
}
.sidebar {
  background: linear-gradient(180deg, #153a68 0%, #0f2949 100%);
  color: white;
  padding: 24px 18px;
}
.brand {
  font-size: 20px;
  font-weight: 800;
  margin-bottom: 24px;
}
.nav-list {
  display: grid;
  gap: 8px;
}
.nav-link {
  padding: 12px 14px;
  border-radius: 10px;
  color: rgba(255,255,255,0.88);
}
.nav-link.router-link-active {
  background: rgba(255,255,255,0.16);
  color: white;
}
.content {
  display: grid;
  grid-template-rows: auto 1fr;
}
.topbar {
  background: rgba(255,255,255,0.85);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--border);
  padding: 14px 24px;
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: center;
}
.user-box {
  display: flex;
  align-items: center;
  gap: 18px;
}
.main-content {
  padding: 24px;
}
@media (max-width: 960px) {
  .main-layout {
    grid-template-columns: 1fr;
  }
  .sidebar {
    padding-bottom: 12px;
  }
}
</style>
