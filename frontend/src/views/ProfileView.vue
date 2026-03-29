<template>
  <div class="page-shell">
    <div class="page-card page-section">
      <AppPageHeader :title="t('profile.title')" />
      <div class="form-grid">
        <AppInput :model-value="auth.user?.full_name || ''" :label="t('profile.fullName')" disabled />
        <AppInput :model-value="auth.user?.username || ''" :label="t('auth.username')" disabled />
        <AppInput :model-value="auth.user?.role || ''" :label="t('profile.role')" disabled />
        <AppInput :model-value="auth.user?.scope_type || ''" :label="t('profile.scope')" disabled />
        <AppInput :model-value="auth.user?.management_name || auth.user?.management || ''" :label="t('profile.management')" disabled />
        <AppInput :model-value="auth.user?.department_name || auth.user?.department || ''" :label="t('profile.department')" disabled />
      </div>
    </div>

    <div class="page-card page-section">
      <AppPageHeader :title="t('profile.title')" :subtitle="t('profile.passwordUpdated')" />
      <div class="form-grid">
        <AppInput v-model="form.current_password" :label="t('profile.currentPassword')" type="password" :error="errors.current_password" />
        <AppInput v-model="form.new_password" :label="t('profile.newPassword')" type="password" :error="errors.new_password" />
        <AppInput v-model="form.new_password_confirm" :label="t('profile.confirmPassword')" type="password" :error="errors.new_password_confirm" />
      </div>
      <p v-if="successMessage" class="success-text">{{ successMessage }}</p>
      <div class="toolbar-row">
        <AppButton @click="submit">{{ t("actions.save") }}</AppButton>
        <AppButton variant="secondary" @click="auth.logout">{{ t("actions.logout") }}</AppButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import { useI18n } from "vue-i18n";

import { authApi } from "@/api/authApi";
import AppButton from "@/components/AppButton.vue";
import AppInput from "@/components/AppInput.vue";
import AppPageHeader from "@/components/AppPageHeader.vue";
import { useAuthStore } from "@/stores/authStore";

const { t } = useI18n();
const auth = useAuthStore();

const form = reactive({
  current_password: "",
  new_password: "",
  new_password_confirm: "",
});

const errors = reactive({
  current_password: "",
  new_password: "",
  new_password_confirm: "",
});

const successMessage = ref("");

async function submit() {
  errors.current_password = form.current_password ? "" : t("validation.required");
  errors.new_password = form.new_password ? "" : t("validation.required");
  errors.new_password_confirm = form.new_password_confirm ? "" : t("validation.required");
  if (form.new_password && form.new_password_confirm && form.new_password !== form.new_password_confirm) {
    errors.new_password_confirm = t("validation.passwordsMustMatch");
  }
  if (errors.current_password || errors.new_password || errors.new_password_confirm) return;

  await authApi.changePassword({
    current_password: form.current_password,
    new_password: form.new_password,
  });
  successMessage.value = t("profile.passwordUpdated");
  form.current_password = "";
  form.new_password = "";
  form.new_password_confirm = "";
}
</script>
