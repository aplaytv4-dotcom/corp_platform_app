<template>
  <AppCrudPage
    ref="pageRef"
    :title="t('menu.departments')"
    :columns="columns"
    :fields="fields"
    :list-fn="departmentsApi.list"
    :create-fn="departmentsApi.create"
    :update-fn="departmentsApi.update"
    :initial-form="config.initialForm"
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
import { computed, onMounted, ref } from "vue";
import { useI18n } from "vue-i18n";

import { departmentsApi } from "@/api/departmentsApi";
import AppButton from "@/components/AppButton.vue";
import AppCrudPage from "@/components/AppCrudPage.vue";
import { useDepartmentsConfig } from "@/modules/departments/config";
import { useReferenceStore } from "@/stores/referenceStore";

const { t } = useI18n();
const pageRef = ref(null);
const referenceStore = useReferenceStore();
const config = useDepartmentsConfig(referenceStore);
const columns = computed(() => [
  ...config.columns.map((column) => ({
    ...column,
    label: t(column.labelKey),
  })),
  { key: "actions", label: "" },
]);
const fields = computed(() =>
  config.fields.map((field) => ({
    ...field,
    label: t(field.labelKey),
  })),
);

onMounted(() => referenceStore.loadManagements());
</script>
