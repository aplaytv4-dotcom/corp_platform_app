<template>
  <div class="page-shell">
    <div class="page-card page-section">
      <AppPageHeader :title="t('menu.assignments')">
        <AppButton @click="openCreate">{{ t("actions.create") }}</AppButton>
        <AppButton variant="secondary" @click="openTransfer">{{ t("assignments.transfer") }}</AppButton>
      </AppPageHeader>
    </div>

    <div class="page-card page-section">
      <div class="form-grid assignments-filters">
        <AppSelect
          v-model="currentFilter"
          :label="t('assignments.currentOnly')"
          :options="filterOptions"
        />
      </div>

      <AppTable :columns="columns" :rows="filteredRows">
        <template #cell-actions="{ row }">
          <div class="toolbar-row">
            <AppButton v-if="row.is_current" variant="danger" @click="closeAssignment(row)">{{ t("assignments.close") }}</AppButton>
          </div>
        </template>
      </AppTable>
    </div>

    <AppModal :open="modalOpen" :title="modalTitle" @close="closeModal">
      <AssignmentForm
        v-model="form"
        :employee-options="employeeOptions"
        :staff-unit-options="staffUnitOptions"
        :position-options="positionOptions"
      />
      <div class="toolbar-row" style="margin-top: 16px;">
        <AppButton @click="submit">{{ t("actions.save") }}</AppButton>
        <AppButton variant="secondary" @click="closeModal">{{ t("actions.cancel") }}</AppButton>
      </div>
    </AppModal>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from "vue";
import { useI18n } from "vue-i18n";

import { assignmentsApi } from "@/api/assignmentsApi";
import { employeesApi } from "@/api/employeesApi";
import { positionsApi } from "@/api/positionsApi";
import { staffUnitsApi } from "@/api/staffUnitsApi";
import AppButton from "@/components/AppButton.vue";
import AppModal from "@/components/AppModal.vue";
import AppPageHeader from "@/components/AppPageHeader.vue";
import AppSelect from "@/components/AppSelect.vue";
import AppTable from "@/components/AppTable.vue";
import AssignmentForm from "@/components/AssignmentForm.vue";

const { t } = useI18n();

const rows = ref([]);
const employees = ref([]);
const positions = ref([]);
const staffUnits = ref([]);
const modalOpen = ref(false);
const mode = ref("create");
const currentFilter = ref("true");

const form = reactive({
  employee: "",
  staff_unit: "",
  actual_position: "",
  start_date: "",
  end_date: "",
  note: "",
});

const columns = computed(() => [
  { key: "employee_name", label: t("assignments.employee") },
  { key: "department_name", label: t("assignments.department") },
  { key: "staff_unit_number", label: t("assignments.staffUnit") },
  { key: "actual_position_name", label: t("assignments.actualPosition") },
  { key: "start_date", label: t("assignments.startDate") },
  { key: "end_date", label: t("assignments.endDate") },
  { key: "is_current", label: t("assignments.current") },
  { key: "actions", label: "" },
]);

const filterOptions = computed(() => [
  { value: "true", label: t("assignments.current") },
  { value: "false", label: t("assignments.closed") },
  { value: "all", label: t("assignments.all") },
]);

const filteredRows = computed(() => {
  if (currentFilter.value === "all") {
    return rows.value;
  }
  const isCurrent = currentFilter.value === "true";
  return rows.value.filter((row) => Boolean(row.is_current) === isCurrent);
});

const modalTitle = computed(() => (mode.value === "transfer" ? t("assignments.transfer") : t("assignments.createAssignment")));

const employeeOptions = computed(() => employees.value.map((item) => ({ value: item.id, label: `${item.short_fio} (${item.personnel_number})` })));
const staffUnitOptions = computed(() => staffUnits.value.map((item) => ({ value: item.id, label: `${item.department_name} / ${item.unit_number}` })));
const positionOptions = computed(() => positions.value.map((item) => ({ value: item.id, label: item.name })));

function resetForm() {
  form.employee = "";
  form.staff_unit = "";
  form.actual_position = "";
  form.start_date = "";
  form.end_date = "";
  form.note = "";
}

async function loadData() {
  const [assignmentsResponse, employeesResponse, positionsResponse, staffUnitsResponse] = await Promise.all([
    assignmentsApi.list(),
    employeesApi.list(),
    positionsApi.list(),
    staffUnitsApi.list(),
  ]);
  rows.value = Array.isArray(assignmentsResponse.data) ? assignmentsResponse.data : assignmentsResponse.data.results || [];
  employees.value = Array.isArray(employeesResponse.data) ? employeesResponse.data : employeesResponse.data.results || [];
  positions.value = Array.isArray(positionsResponse.data) ? positionsResponse.data : positionsResponse.data.results || [];
  staffUnits.value = Array.isArray(staffUnitsResponse.data) ? staffUnitsResponse.data : staffUnitsResponse.data.results || [];
}

function openCreate() {
  resetForm();
  mode.value = "create";
  modalOpen.value = true;
}

function openTransfer() {
  resetForm();
  mode.value = "transfer";
  modalOpen.value = true;
}

function closeModal() {
  modalOpen.value = false;
}

async function submit() {
  const payload = { ...form };
  if (mode.value === "transfer") {
    await assignmentsApi.transfer({
      employee: payload.employee,
      new_staff_unit: payload.staff_unit,
      actual_position: payload.actual_position,
      start_date: payload.start_date,
      note: payload.note,
    });
  } else {
    await assignmentsApi.create(payload);
  }
  closeModal();
  await loadData();
}

async function closeAssignment(row) {
  await assignmentsApi.close(row.id, {
    end_date: new Date().toISOString().slice(0, 10),
    is_current: false,
  });
  await loadData();
}

onMounted(loadData);
</script>

<style scoped>
.assignments-filters {
  margin-bottom: 16px;
  max-width: 240px;
}
</style>
