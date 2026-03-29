<template>
  <tr>
    <td>{{ index + 1 }}</td>
    <td>{{ row.actual_position_name || row.position_name || "—" }}</td>
    <td>{{ row.employee_name }}</td>
    <td>
      <AppSelect v-model="localRow.status" :options="statusOptions" @update:model-value="emitUpdate" />
    </td>
    <td>
      <AppSelect
        v-if="localRow.status === 'absent'"
        v-model="localRow.absence_reason"
        :options="reasonOptions"
        @update:model-value="emitUpdate"
      />
      <span v-else class="muted">—</span>
    </td>
    <td>
      <AppTextarea v-model="localRow.note" compact rows="1" class="attendance-note" @update:model-value="emitUpdate" />
    </td>
  </tr>
</template>

<script setup>
import { reactive, watch } from "vue";
import { useI18n } from "vue-i18n";

import AppSelect from "./AppSelect.vue";
import AppTextarea from "./AppTextarea.vue";

const props = defineProps({
  row: { type: Object, required: true },
  index: { type: Number, required: true },
  reasonOptions: { type: Array, default: () => [] },
});

const emit = defineEmits(["update"]);
const { t } = useI18n();

const localRow = reactive({ ...props.row });

watch(
  () => props.row,
  (value) => Object.assign(localRow, value),
  { deep: true },
);

const statusOptions = [
  { value: "present", label: t("attendance.present") },
  { value: "absent", label: t("attendance.absent") },
];

watch(
  () => localRow.status,
  (value) => {
    if (value === "present") {
      localRow.absence_reason = null;
      localRow.note = "";
      emitUpdate();
    }
  },
);

function emitUpdate() {
  emit("update", { ...localRow });
}
</script>

<style scoped>
.attendance-note {
  min-width: 150px;
  max-width: 170px;
}
</style>
