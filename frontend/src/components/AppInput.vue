<template>
  <label class="field">
    <span v-if="label" class="field-label">{{ label }}</span>
    <input class="field-control" :value="modelValue" @input="$emit('update:modelValue', $event.target.value)" v-bind="$attrs" />
    <span v-if="error" class="field-error">{{ error }}</span>
  </label>
</template>

<script setup>
defineProps({
  modelValue: { type: [String, Number], default: "" },
  label: { type: String, default: "" },
  error: { type: String, default: "" },
});
defineEmits(["update:modelValue"]);
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
