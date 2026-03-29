<template>
  <div class="table-wrap">
    <table class="app-table">
      <thead>
        <tr>
          <th v-for="column in columns" :key="column.key">{{ column.label }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="!rows.length">
          <td :colspan="columns.length">
            <slot name="empty">
              <div class="muted">No data</div>
            </slot>
          </td>
        </tr>
        <tr v-for="(row, index) in rows" :key="row.id || index">
          <td v-for="column in columns" :key="column.key">
            <slot :name="`cell-${column.key}`" :row="row" :index="index">
              <AppStatusBadge
                v-if="isBooleanColumn(row[column.key])"
                :label="row[column.key] ? activeLabel : inactiveLabel"
                :tone="row[column.key] ? 'success' : 'danger'"
              />
              <template v-else>
                {{ row[column.key] }}
              </template>
            </slot>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import AppStatusBadge from "./AppStatusBadge.vue";

defineProps({
  columns: { type: Array, default: () => [] },
  rows: { type: Array, default: () => [] },
});

const activeLabel = "\u0410\u043a\u0442\u0438\u0432\u0435\u043d";
const inactiveLabel = "\u041d\u0435\u0430\u043a\u0442\u0438\u0432\u0435\u043d";

function isBooleanColumn(value) {
  return typeof value === "boolean";
}
</script>

<style scoped>
.app-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}
.app-table th,
.app-table td {
  padding: 12px 10px;
  border-bottom: 1px solid var(--border);
  vertical-align: top;
}
.app-table th {
  background: #f5f7fb;
  text-align: left;
  font-size: 13px;
  color: var(--text-soft);
}
</style>
