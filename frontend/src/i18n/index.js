import { createI18n } from "vue-i18n";

import { storage } from "@/utils/storage";
import { messages } from "./messages";

const locale = storage.get("ui.language", "ru");

const i18n = createI18n({
  legacy: false,
  locale,
  fallbackLocale: "ru",
  messages,
});

export default i18n;
