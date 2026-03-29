<template>
  <label class="field">
    <span v-if="label" class="field-label">{{ label }}</span>
    <textarea
      :class="['field-control', 'textarea', { 'textarea-compact': compact }]"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      v-bind="$attrs"
    />
    <span v-if="error" class="field-error">{{ error }}</span>
  </label>
</template>

<script setup>
defineProps({
  modelValue: { type: String, default: "" },
  label: { type: String, default: "" },
  error: { type: String, default: "" },
  compact: { type: Boolean, default: false },
});
defineEmits(["update:modelValue"]);
</script>

<style scoped>
.field { display: grid; gap: 6px; }
.field-label { font-size: 14px; font-weight: 600; color: var(--text); }
.field-control {
  width: 100%;
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid var(--border);
  background: white;
}
.textarea { min-height: 100px; resize: vertical; }
.textarea-compact { min-height: 42px; height: 42px; resize: none; }
.field-error { color: var(--danger); font-size: 13px; }
</style>
