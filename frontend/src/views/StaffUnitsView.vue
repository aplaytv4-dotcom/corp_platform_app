<template>
  <AppCrudPage
    ref="pageRef"
    :title="t('menu.staffUnits')"
    :columns="columns"
    :fields="config.fields"
    :list-fn="staffUnitsApi.list"
    :create-fn="staffUnitsApi.create"
    :update-fn="staffUnitsApi.update"
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

import { staffUnitsApi } from "@/api/staffUnitsApi";
import AppButton from "@/components/AppButton.vue";
import AppCrudPage from "@/components/AppCrudPage.vue";
import { useStaffUnitsConfig } from "@/modules/staff-units/config";
import { useReferenceStore } from "@/stores/referenceStore";

const { t } = useI18n();
const pageRef = ref(null);
const referenceStore = useReferenceStore();
const config = useStaffUnitsConfig(referenceStore);
const columns = computed(() => [...config.columns, { key: "actions", label: "" }]);

onMounted(async () => {
  await Promise.all([referenceStore.loadDepartments(), referenceStore.loadPositions()]);
});
</script>
