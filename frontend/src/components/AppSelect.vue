<template>
  <label class="field">
    <span v-if="label" class="field-label">{{ label }}</span>
    <select class="field-control" :value="selectedValue" @change="handleChange" v-bind="$attrs">
      <option value="">{{ placeholder }}</option>
      <option v-for="option in options" :key="String(option.value)" :value="String(option.value)">
        {{ option.label }}
      </option>
    </select>
    <span v-if="error" class="field-error">{{ error }}</span>
  </label>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  modelValue: { type: [String, Number], default: "" },
  label: { type: String, default: "" },
  placeholder: { type: String, default: "" },
  options: { type: Array, default: () => [] },
  error: { type: String, default: "" },
});
const emit = defineEmits(["update:modelValue"]);

const selectedValue = computed(() => String(props.modelValue ?? ""));

function handleChange(event) {
  const rawValue = event.target.value;
  const option = props.options.find((item) => String(item.value) === rawValue);
  emit("update:modelValue", option ? option.value : rawValue);
}
</script>

<style scoped>
.field { display: grid; gap: 6px; }
.field-label { font-size: 14px; font-weight: 600; color: var(--text); }
.field-control {
  width: 100%;
  min-height: 42px;
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid var(--border);
  background: white;
}
.field-error { color: var(--danger); font-size: 13px; }
</style>
