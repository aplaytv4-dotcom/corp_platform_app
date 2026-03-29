<template>
  <div class="empty-state">
    <h3>{{ title }}</h3>
    <p class="muted">{{ description }}</p>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, default: "Нет данных" },
  description: { type: String, default: "" },
});
</script>

<style scoped>
.empty-state {
  padding: 28px;
  text-align: center;
}
</style>
