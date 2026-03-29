<template>
  <div class="page-card page-section">
    <AppEmptyState :title="t('common.forbidden')" description="403" />
    <div class="toolbar-row">
      <AppButton @click="$router.push('/attendance')">{{ t("actions.back") }}</AppButton>
    </div>
  </div>
</template>

<script setup>
import { useI18n } from "vue-i18n";

import AppButton from "@/components/AppButton.vue";
import AppEmptyState from "@/components/AppEmptyState.vue";

const { t } = useI18n();
</script>
