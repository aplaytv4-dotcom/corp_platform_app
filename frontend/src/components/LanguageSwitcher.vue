<template>
  <div class="switcher">
    <button :class="{ active: modelValue === 'ru' }" @click="$emit('update:modelValue', 'ru')">RU</button>
    <button :class="{ active: modelValue === 'uz' }" @click="$emit('update:modelValue', 'uz')">UZ</button>
  </div>
</template>

<script setup>
defineProps({
  modelValue: { type: String, default: "ru" },
});
defineEmits(["update:modelValue"]);
</script>

<style scoped>
.switcher {
  display: inline-flex;
  border: 1px solid var(--border);
  border-radius: 999px;
  overflow: hidden;
}
.switcher button {
  border: 0;
  background: white;
  padding: 8px 12px;
  cursor: pointer;
}
.switcher button.active {
  background: var(--primary);
  color: white;
}
</style>
