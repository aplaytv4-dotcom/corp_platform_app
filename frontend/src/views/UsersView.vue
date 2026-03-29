<template>
  <AppCrudPage
    ref="pageRef"
    :title="t('menu.users')"
    :columns="columns"
    :fields="fields"
    :list-fn="usersApi.list"
    :create-fn="usersApi.create"
    :update-fn="usersApi.update"
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

import { usersApi } from "@/api/usersApi";
import AppButton from "@/components/AppButton.vue";
import AppCrudPage from "@/components/AppCrudPage.vue";
import { useUsersConfig } from "@/modules/users/config";
import { useReferenceStore } from "@/stores/referenceStore";

const { t } = useI18n();
const pageRef = ref(null);
const referenceStore = useReferenceStore();
const config = useUsersConfig(referenceStore);

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
    options: Array.isArray(field.options)
      ? field.options.map((option) => ({
          ...option,
          label: option.labelKey ? t(option.labelKey) : option.label,
        }))
      : field.options,
  })),
);

onMounted(async () => {
  await Promise.all([referenceStore.loadDepartments(), referenceStore.loadManagements()]);
});
</script>
