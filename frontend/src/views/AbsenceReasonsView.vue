<template>
  <AppCrudPage
    ref="pageRef"
    :title="t('menu.absenceReasons')"
    :columns="columns"
    :fields="config.fields"
    :list-fn="absenceReasonsApi.list"
    :create-fn="absenceReasonsApi.create"
    :update-fn="auth.isAdmin ? absenceReasonsApi.update : null"
    :initial-form="config.initialForm"
    :can-create="true"
    :can-edit="auth.isAdmin"
    :custom-cell-keys="['actions']"
  >
    <template #cell-actions="{ row }">
      <AppButton v-if="auth.isAdmin" variant="secondary" @click="pageRef.startEdit(row)">{{ t("actions.edit") }}</AppButton>
    </template>
  </AppCrudPage>
</template>

<script setup>
import { computed, ref } from "vue";
import { useI18n } from "vue-i18n";

import { absenceReasonsApi } from "@/api/absenceReasonsApi";
import AppButton from "@/components/AppButton.vue";
import AppCrudPage from "@/components/AppCrudPage.vue";
import { absenceReasonsConfig as config } from "@/modules/absence-reasons/config";
import { useAuthStore } from "@/stores/authStore";

const { t } = useI18n();
const auth = useAuthStore();
const pageRef = ref(null);

const columns = computed(() => [...config.columns, { key: "actions", label: "" }]);
</script>
