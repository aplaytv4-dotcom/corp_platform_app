<template>
  <button :class="['app-button', variant, { block }]" :type="type" :disabled="disabled || loading" v-bind="$attrs">
    <span v-if="loading">...</span>
    <span v-else><slot /></span>
  </button>
</template>

<script setup>
defineProps({
  type: { type: String, default: "button" },
  variant: { type: String, default: "primary" },
  loading: { type: Boolean, default: false },
  disabled: { type: Boolean, default: false },
  block: { type: Boolean, default: false },
});
</script>

<style scoped>
.app-button {
  border: 0;
  border-radius: 10px;
  padding: 10px 16px;
  cursor: pointer;
  transition: 0.2s ease;
  font-weight: 600;
}
.app-button.primary { background: var(--primary); color: white; }
.app-button.primary:hover { background: var(--primary-hover); }
.app-button.secondary { background: var(--surface-muted); color: var(--text); border: 1px solid var(--border); }
.app-button.danger { background: var(--danger); color: white; }
.app-button.block { width: 100%; }
.app-button:disabled { opacity: 0.6; cursor: not-allowed; }
</style>
