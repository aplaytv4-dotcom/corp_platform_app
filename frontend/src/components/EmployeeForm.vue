<template>
  <div class="form-grid">
    <AppInput v-model="form.last_name" :label="'Last name'" />
    <AppInput v-model="form.first_name" :label="'First name'" />
    <AppInput v-model="form.middle_name" :label="'Middle name'" />
    <AppInput v-model="form.personnel_number" :label="'Personnel number'" />
    <AppSelect v-model="form.is_active" :label="'Status'" :options="statusOptions" />
  </div>
</template>

<script setup>
import { computed } from "vue";

import AppInput from "./AppInput.vue";
import AppSelect from "./AppSelect.vue";

const props = defineProps({
  modelValue: { type: Object, required: true },
});
const emit = defineEmits(["update:modelValue"]);

const form = computed({
  get: () => props.modelValue,
  set: (value) => emit("update:modelValue", value),
});

const statusOptions = [
  { value: true, label: "Active" },
  { value: false, label: "Inactive" },
];
</script>
