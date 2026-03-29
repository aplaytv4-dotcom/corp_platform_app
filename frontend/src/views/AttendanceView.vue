<template>
  <div class="page-shell">
    <div class="page-card page-section">
      <AppPageHeader :title="t('attendance.title')" />
      <div class="form-grid">
        <AppInput v-model="attendance.selectedDate" :label="t('attendance.date')" type="date" :error="errors.date" />
        <AppSelect
          v-if="showDepartmentSelect"
          v-model="attendance.selectedDepartment"
          :label="t('attendance.department')"
          :options="departmentOptions"
          :error="errors.department"
        />
      </div>
      <div class="toolbar-row" style="margin-top: 16px;">
        <AppButton :loading="attendance.loading" @click="openSheet">{{ t("actions.open") }}</AppButton>
        <AppButton variant="secondary" @click="openPreview">{{ t("actions.preview") }}</AppButton>
      </div>
    </div>

    <div class="page-card page-section">
      <AppLoader v-if="attendance.loading" :label="t('common.loading')" />
      <AppEmptyState v-else-if="!attendance.items.length" :title="t('common.empty')" />
      <AttendanceTable
        v-else
        :rows="attendance.items"
        :reason-options="reasonOptions"
        @update-row="updateRow"
      />
      <div v-if="attendance.items.length" class="toolbar-row" style="margin-top: 16px;">
        <AppButton :loading="attendance.saving" @click="save">{{ t("actions.save") }}</AppButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive } from "vue";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";

import AppButton from "@/components/AppButton.vue";
import AppEmptyState from "@/components/AppEmptyState.vue";
import AppInput from "@/components/AppInput.vue";
import AppLoader from "@/components/AppLoader.vue";
import AppPageHeader from "@/components/AppPageHeader.vue";
import AppSelect from "@/components/AppSelect.vue";
import AttendanceTable from "@/components/AttendanceTable.vue";
import { useAttendanceStore } from "@/stores/attendanceStore";
import { useReferenceStore } from "@/stores/referenceStore";

const { t } = useI18n();
const router = useRouter();
const attendance = useAttendanceStore();
const referenceStore = useReferenceStore();

const errors = reactive({
  date: "",
  department: "",
});

const departmentOptions = computed(() =>
  referenceStore.departments.map((item) => ({ value: item.id, label: item.name })),
);

const reasonOptions = computed(() =>
  referenceStore.absenceReasons.map((item) => ({ value: item.id, label: item.name })),
);

const showDepartmentSelect = computed(() => referenceStore.departments.length > 1);

async function bootstrap() {
  await Promise.all([
    referenceStore.loadDepartments(),
    referenceStore.loadAbsenceReasons(),
  ]);
  if (!attendance.selectedDepartment && referenceStore.departments.length === 1) {
    attendance.selectedDepartment = referenceStore.departments[0].id;
  }
}

function validate() {
  errors.date = attendance.selectedDate ? "" : t("validation.required");
  errors.department = showDepartmentSelect.value && !attendance.selectedDepartment ? t("validation.departmentRequired") : "";
  return !(errors.date || errors.department);
}

async function openSheet() {
  if (!validate()) return;
  return attendance.openOrCreateSheet();
}

async function save() {
  const invalidAbsent = attendance.items.some((item) => item.status === "absent" && !item.absence_reason);
  if (invalidAbsent) {
    errors.department = t("validation.absenceReasonRequired");
    return;
  }
  await attendance.saveSheet();
}

function updateRow(index, nextRow) {
  attendance.items[index] = nextRow;
}

async function openPreview() {
  if (!validate()) return;
  if (!attendance.currentSheet?.id || attendance.currentSheet?.date !== attendance.selectedDate || String(attendance.currentSheet?.department) !== String(attendance.selectedDepartment)) {
    await openSheet();
  }
  const query = {
    type: "daily",
  };
  if (attendance.currentSheet?.id) {
    query.sheet_id = attendance.currentSheet.id;
  } else {
    query.start_date = attendance.selectedDate;
    query.end_date = attendance.selectedDate;
  }
  router.push({ path: "/reports/preview", query });
}

onMounted(bootstrap);
</script>
