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
        <AppInput
          v-else
          :model-value="currentDepartmentName"
          :label="t('attendance.department')"
          disabled
        />
      </div>
      <div class="toolbar-row" style="margin-top: 16px;">
        <AppButton :loading="attendance.loading" @click="openSheet">{{ t("actions.open") }}</AppButton>
        <AppButton variant="secondary" @click="openPreview">{{ t("actions.preview") }}</AppButton>
      </div>
    </div>

    <div class="page-card page-section">
      <AppPageHeader :title="t('reports.summary')" :subtitle="t('reports.periodHint')" />
      <div class="form-grid">
        <AppInput v-model="summaryStartDate" :label="t('reports.periodStart')" type="date" :error="errors.summaryStartDate" />
        <AppInput v-model="summaryEndDate" :label="t('reports.periodEnd')" type="date" :error="errors.summaryEndDate" />
      </div>
      <p v-if="errors.summaryRange" class="danger-text" style="margin-top: 16px;">{{ errors.summaryRange }}</p>
      <div class="toolbar-row" style="margin-top: 16px;">
        <AppButton variant="secondary" @click="openSummaryPreview">{{ t("actions.preview") }}</AppButton>
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
      <p v-if="successMessage" class="success-text" style="margin-top: 16px;">{{ successMessage }}</p>
      <p v-if="errors.save" class="danger-text" style="margin-top: 16px;">{{ errors.save }}</p>
      <div v-if="attendance.items.length" class="toolbar-row" style="margin-top: 16px;">
        <AppButton :loading="attendance.saving" @click="save">{{ t("actions.save") }}</AppButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from "vue";
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
import { normalizeApiError } from "@/utils/apiErrors";

const { t } = useI18n();
const router = useRouter();
const attendance = useAttendanceStore();
const referenceStore = useReferenceStore();
const successMessage = ref("");
const summaryStartDate = ref(attendance.selectedDate);
const summaryEndDate = ref(attendance.selectedDate);

const errors = reactive({
  date: "",
  department: "",
  summaryStartDate: "",
  summaryEndDate: "",
  summaryRange: "",
  save: "",
});

const activeDepartments = computed(() =>
  referenceStore.departments.filter((item) => item.is_active),
);

const departmentOptions = computed(() =>
  activeDepartments.value.map((item) => ({ value: item.id, label: item.name })),
);

const activeAbsenceReasons = computed(() =>
  referenceStore.absenceReasons.filter((item) => item.is_active),
);

const reasonOptions = computed(() =>
  activeAbsenceReasons.value.map((item) => ({ value: item.id, label: item.name })),
);

const showDepartmentSelect = computed(() => activeDepartments.value.length > 1);
const currentDepartmentName = computed(() =>
  activeDepartments.value.find((item) => String(item.id) === String(attendance.selectedDepartment))?.name || "",
);

async function bootstrap() {
  await Promise.all([
    referenceStore.loadDepartments(),
    referenceStore.loadAbsenceReasons(),
  ]);

  const hasSelectedActiveDepartment = activeDepartments.value.some(
    (item) => String(item.id) === String(attendance.selectedDepartment),
  );

  if (!hasSelectedActiveDepartment) {
    attendance.selectedDepartment = activeDepartments.value[0]?.id || "";
  }
}

function validate() {
  errors.date = attendance.selectedDate ? "" : t("validation.required");
  errors.department = showDepartmentSelect.value && !attendance.selectedDepartment ? t("validation.departmentRequired") : "";
  errors.save = "";
  return !(errors.date || errors.department);
}

function validateSummaryRange() {
  errors.summaryStartDate = summaryStartDate.value ? "" : t("validation.required");
  errors.summaryEndDate = summaryEndDate.value ? "" : t("validation.required");
  errors.summaryRange = "";

  if (errors.summaryStartDate || errors.summaryEndDate) {
    return false;
  }

  if (summaryStartDate.value > summaryEndDate.value) {
    errors.summaryRange = t("validation.dateRangeInvalid");
    return false;
  }

  return true;
}

async function openSheet() {
  if (!validate()) return;
  successMessage.value = "";
  const result = await attendance.openOrCreateSheet();
  sanitizeInactiveAbsenceReasons();
  return result;
}

async function save() {
  successMessage.value = "";
  errors.save = "";
  const invalidAbsent = attendance.items.some((item) => item.status === "absent" && !item.absence_reason);
  if (invalidAbsent) {
    errors.save = t("validation.absenceReasonRequired");
    return;
  }
  try {
    await attendance.saveSheet();
  } catch (error) {
    errors.save = normalizeApiError(error, {
      fallbackMessage: t("attendance.saveFailed"),
      t,
    });
    return;
  }
  successMessage.value = t("attendance.saveSuccess");
}

function updateRow(index, nextRow) {
  attendance.items[index] = nextRow;
}

function sanitizeInactiveAbsenceReasons() {
  const activeReasonIds = new Set(activeAbsenceReasons.value.map((item) => String(item.id)));
  let hasInactiveReason = false;

  attendance.items = attendance.items.map((item) => {
    if (item.status !== "absent" || !item.absence_reason) {
      return item;
    }
    if (activeReasonIds.has(String(item.absence_reason))) {
      return item;
    }
    hasInactiveReason = true;
    return {
      ...item,
      absence_reason: null,
    };
  });

  if (hasInactiveReason) {
    errors.save = t("attendance.inactiveAbsenceReasons");
  }
}

async function openPreview() {
  if (!validate()) return;
  if (
    !attendance.currentSheet?.id ||
    attendance.currentSheet?.date !== attendance.selectedDate ||
    String(attendance.currentSheet?.department) !== String(attendance.selectedDepartment)
  ) {
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

function openSummaryPreview() {
  if (!validateSummaryRange()) return;
  router.push({
    path: "/reports/preview",
    query: {
      type: "summary",
      start_date: summaryStartDate.value,
      end_date: summaryEndDate.value,
    },
  });
}

onMounted(bootstrap);
</script>
