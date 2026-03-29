<template>
  <div class="form-grid">
    <AppSelect v-model="form.employee" :label="t('assignments.employee')" :options="employeeOptions" />
    <AppSelect v-model="form.staff_unit" :label="t('assignments.staffUnit')" :options="staffUnitOptions" />
    <AppSelect v-model="form.actual_position" :label="t('assignments.actualPosition')" :options="positionOptions" />
    <AppInput v-model="form.start_date" :label="t('assignments.startDate')" type="date" />
    <AppInput v-model="form.end_date" :label="t('assignments.endDate')" type="date" />
    <AppTextarea v-model="form.note" :label="t('attendance.note')" />
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useI18n } from "vue-i18n";

import AppInput from "./AppInput.vue";
import AppSelect from "./AppSelect.vue";
import AppTextarea from "./AppTextarea.vue";

const props = defineProps({
  modelValue: { type: Object, required: true },
  employeeOptions: { type: Array, default: () => [] },
  staffUnitOptions: { type: Array, default: () => [] },
  positionOptions: { type: Array, default: () => [] },
});

const emit = defineEmits(["update:modelValue"]);
const { t } = useI18n();

const form = computed({
  get: () => props.modelValue,
  set: (value) => emit("update:modelValue", value),
});
</script>
