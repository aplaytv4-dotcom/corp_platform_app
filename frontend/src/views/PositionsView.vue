<template>
  <AppCrudPage
    ref="pageRef"
    :title="t('menu.positions')"
    :columns="columns"
    :fields="fields"
    :list-fn="positionsApi.list"
    :create-fn="positionsApi.create"
    :update-fn="positionsApi.update"
    :initial-form="positionsConfig.initialForm"
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

import { positionsApi } from "@/api/positionsApi";
import AppButton from "@/components/AppButton.vue";
import AppCrudPage from "@/components/AppCrudPage.vue";
import { positionsConfig } from "@/modules/positions/config";

const { t } = useI18n();
const pageRef = ref(null);
const columns = computed(() => [
  ...positionsConfig.columns.map((column) => ({
    ...column,
    label: t(column.labelKey),
  })),
  { key: "actions", label: "" },
]);

const fields = computed(() =>
  positionsConfig.fields.map((field) => ({
    ...field,
    label: t(field.labelKey),
  })),
);
</script>
