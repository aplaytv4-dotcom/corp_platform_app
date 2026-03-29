<template>
  <div class="table-wrap">
    <table class="app-table">
      <thead>
        <tr>
          <th>{{ t("attendance.number") }}</th>
          <th>{{ t("attendance.actualPosition") }}</th>
          <th>{{ t("attendance.fio") }}</th>
          <th>{{ t("attendance.status") }}</th>
          <th>{{ t("attendance.absenceReason") }}</th>
          <th>{{ t("attendance.note") }}</th>
        </tr>
      </thead>
      <tbody>
        <AttendanceRow
          v-for="(row, index) in rows"
          :key="row.id || row.employee"
          :row="row"
          :index="index"
          :reason-options="reasonOptions"
          @update="$emit('update-row', index, $event)"
        />
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { useI18n } from "vue-i18n";

import AttendanceRow from "./AttendanceRow.vue";

defineProps({
  rows: { type: Array, default: () => [] },
  reasonOptions: { type: Array, default: () => [] },
});

defineEmits(["update-row"]);

const { t } = useI18n();
</script>
