import { defineStore } from "pinia";

import i18n from "@/i18n";
import { storage } from "@/utils/storage";

export const useUiStore = defineStore("ui", {
  state: () => ({
    currentLanguage: storage.get("ui.language", "ru"),
    sidebarOpen: true,
  }),
  actions: {
    setLanguage(language) {
      this.currentLanguage = language;
      storage.set("ui.language", language);
      i18n.global.locale.value = language;
    },
    toggleSidebar() {
      this.sidebarOpen = !this.sidebarOpen;
    },
  },
});
