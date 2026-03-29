<template>
  <span :class="['status-badge', tone]"><slot>{{ label }}</slot></span>
</template>

<script setup>
defineProps({
  label: { type: String, default: "" },
  tone: { type: String, default: "neutral" },
});
</script>

<style scoped>
.status-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
}
.neutral { background: #edf2f7; color: #334155; }
.success { background: #dcfce7; color: #166534; }
.danger { background: #fee2e2; color: #991b1b; }
.warning { background: #ffedd5; color: #9a3412; }
</style>
