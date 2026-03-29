<template>
  <div class="loader">{{ label }}</div>
</template>

<script setup>
defineProps({
  label: { type: String, default: "Loading..." },
});
</script>

<style scoped>
.loader {
  padding: 20px;
  text-align: center;
  color: var(--text-soft);
}
</style>
