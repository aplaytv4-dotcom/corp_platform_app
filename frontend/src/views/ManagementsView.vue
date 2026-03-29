<template>
  <AppCrudPage
    ref="pageRef"
    :title="t('menu.managements')"
    :columns="columns"
    :fields="fields"
    :list-fn="managementsApi.list"
    :create-fn="managementsApi.create"
    :update-fn="managementsApi.update"
    :initial-form="managementsConfig.initialForm"
    :can-create="true"
    :can-edit="true"
    :custom-cell-keys="['actions']"
  >
    <template #cell-actions="{ row }">
      <AppButton variant="secondary" @click="pageRef.startEdit(row)">{{ t("actions.edit") }}</AppButton>
    </template>
  </AppCrudPage>
</template>

<script setup>
import { computed, ref } from "vue";
import { useI18n } from "vue-i18n";

import { managementsApi } from "@/api/managementsApi";
import AppButton from "@/components/AppButton.vue";
import AppCrudPage from "@/components/AppCrudPage.vue";
import { managementsConfig } from "@/modules/managements/config";

const { t } = useI18n();
const pageRef = ref(null);
const columns = computed(() => [
  ...managementsConfig.columns.map((column) => ({
    ...column,
    label: t(column.labelKey),
  })),
  { key: "actions", label: "" },
]);
const fields = computed(() =>
  managementsConfig.fields.map((field) => ({
    ...field,
    label: t(field.labelKey),
  })),
);
</script>
