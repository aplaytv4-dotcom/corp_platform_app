<template>
  <div class="page-shell">
    <AppPageHeader :title="t('appName')" :subtitle="t('actions.login')" />
    <div class="form-grid">
      <AppInput v-model="form.username" :label="t('auth.username')" :error="errors.username" />
      <AppInput v-model="form.password" :label="t('auth.password')" type="password" :error="errors.password" />
    </div>
    <p v-if="errorMessage" class="danger-text">{{ errorMessage }}</p>
    <AppButton block :loading="auth.loading" @click="submit">{{ t("actions.login") }}</AppButton>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import { useI18n } from "vue-i18n";

import AppButton from "@/components/AppButton.vue";
import AppInput from "@/components/AppInput.vue";
import AppPageHeader from "@/components/AppPageHeader.vue";
import { useAuthStore } from "@/stores/authStore";

const { t } = useI18n();
const auth = useAuthStore();

const form = reactive({
  username: "",
  password: "",
});

const errors = reactive({
  username: "",
  password: "",
});

const errorMessage = ref("");

async function submit() {
  errors.username = form.username ? "" : t("validation.required");
  errors.password = form.password ? "" : t("validation.required");
  if (errors.username || errors.password) return;

  errorMessage.value = "";
  try {
    await auth.login(form);
  } catch {
    errorMessage.value = t("auth.invalid");
  }
}
</script>
