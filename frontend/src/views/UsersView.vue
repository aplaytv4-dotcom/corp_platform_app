<template>
  <AppCrudPage
    ref="pageRef"
    :title="t('menu.users')"
    :columns="columns"
    :fields="config.fields"
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

const columns = computed(() => [...config.columns, { key: "actions", label: "" }]);

onMounted(async () => {
  await Promise.all([referenceStore.loadDepartments(), referenceStore.loadManagements()]);
});
</script>
