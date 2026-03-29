<template>
  <div class="form-grid">
    <AppSelect v-model="form.employee" :label="'Employee'" :options="employeeOptions" />
    <AppSelect v-model="form.staff_unit" :label="'Staff unit'" :options="staffUnitOptions" />
    <AppSelect v-model="form.actual_position" :label="'Actual position'" :options="positionOptions" />
    <AppInput v-model="form.start_date" :label="'Start date'" type="date" />
    <AppInput v-model="form.end_date" :label="'End date'" type="date" />
    <AppTextarea v-model="form.note" :label="'Note'" />
  </div>
</template>

<script setup>
import { computed } from "vue";

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

const form = computed({
  get: () => props.modelValue,
  set: (value) => emit("update:modelValue", value),
});
</script>
