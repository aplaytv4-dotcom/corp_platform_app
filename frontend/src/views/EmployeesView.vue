<template>
  <AppCrudPage
    ref="pageRef"
    :title="t('menu.employees')"
    :subtitle="auth.isAdmin ? t('employees.subtitleAdmin') : t('employees.subtitleReadonly')"
    :columns="columns"
    :filters="filters"
    :fields="[]"
    :list-fn="employeesApi.list"
    :create-fn="auth.isAdmin ? employeesApi.create : null"
    :update-fn="auth.isAdmin ? employeesApi.update : null"
    :initial-form="initialForm"
    :can-create="auth.isAdmin"
    :can-edit="auth.isAdmin"
    :custom-form-component="EmployeeForm"
    :custom-cell-keys="['full_name', 'actions']"
  >
    <template #cell-full_name="{ row }">
      {{ [row.last_name, row.first_name, row.middle_name].filter(Boolean).join(" ") }}
    </template>
    <template #cell-actions="{ row }">
      <AppButton v-if="auth.isAdmin" variant="secondary" @click="pageRef.startEdit(row)">{{ t("actions.edit") }}</AppButton>
    </template>
  </AppCrudPage>
</template>

<script setup>
import { computed, ref } from "vue";
import { useI18n } from "vue-i18n";

import { employeesApi } from "@/api/employeesApi";
import AppButton from "@/components/AppButton.vue";
import AppCrudPage from "@/components/AppCrudPage.vue";
import EmployeeForm from "@/components/EmployeeForm.vue";
import { employeeFilters } from "@/modules/employees/config";
import { useAuthStore } from "@/stores/authStore";

const { t } = useI18n();
const auth = useAuthStore();
const pageRef = ref(null);

const columns = computed(() => [
  { key: "full_name", label: t("attendance.fio") },
  { key: "short_fio", label: t("employees.shortFio") },
  { key: "personnel_number", label: t("employees.personnelNumber") },
  { key: "department_name", label: t("employees.department") },
  { key: "staff_position_name", label: t("employees.staffPosition") },
  { key: "actual_position_name", label: t("employees.actualPosition") },
  { key: "is_active", label: t("employees.isActive") },
  { key: "actions", label: "" },
]);

const initialForm = {
  last_name: "",
  first_name: "",
  middle_name: "",
  personnel_number: "",
  is_active: true,
};

const filters = computed(() =>
  employeeFilters.map((filter) => ({
    ...filter,
    label: filter.labelKey ? t(filter.labelKey) : filter.label,
  })),
);
</script>
