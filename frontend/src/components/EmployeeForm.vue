<template>
  <div class="form-grid">
    <AppInput v-model="form.last_name" :label="lastNameLabel" />
    <AppInput v-model="form.first_name" :label="firstNameLabel" />
    <AppInput v-model="form.middle_name" :label="middleNameLabel" />
    <AppInput v-model="form.personnel_number" :label="personnelNumberLabel" />
    <AppSelect v-model="form.is_active" :label="statusLabel" :options="statusOptions" />
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useI18n } from "vue-i18n";

import AppInput from "./AppInput.vue";
import AppSelect from "./AppSelect.vue";

const props = defineProps({
  modelValue: { type: Object, required: true },
});
const emit = defineEmits(["update:modelValue"]);
const { t } = useI18n();

const form = computed({
  get: () => props.modelValue,
  set: (value) => emit("update:modelValue", value),
});

const lastNameLabel = computed(() => t("employees.lastName"));
const firstNameLabel = computed(() => t("employees.firstName"));
const middleNameLabel = computed(() => t("employees.middleName"));
const personnelNumberLabel = computed(() => t("employees.personnelNumber"));
const statusLabel = computed(() => t("employees.status"));

const statusOptions = computed(() => [
  { value: true, label: t("common.active") },
  { value: false, label: t("common.inactive") },
]);
</script>
