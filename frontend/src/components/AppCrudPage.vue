<template>
  <div class="page-shell">
    <div class="page-card page-section">
      <AppPageHeader :title="title" :subtitle="subtitle">
        <AppButton v-if="canCreate" @click="openCreate">{{ resolvedCreateLabel }}</AppButton>
      </AppPageHeader>
    </div>

    <div class="page-card page-section">
      <div v-if="filters?.length" class="form-grid" style="margin-bottom: 16px;">
        <component
          :is="resolveComponent(filter.component)"
          v-for="filter in filters"
          :key="filter.key"
          v-model="filterState[filter.key]"
          :label="filter.label"
          :options="resolveOptions(filter)"
          :placeholder="filter.placeholder || ''"
        />
      </div>
      <p v-if="successMessage" class="success-text" style="margin-bottom: 16px;">{{ successMessage }}</p>

      <AppLoader v-if="loading" />
      <AppTable v-else :columns="columns" :rows="filteredRows">
        <template #empty>
          <AppEmptyState :title="emptyTitle" />
        </template>
        <template v-for="column in customCellKeys" #[`cell-${column}`]="slotProps">
          <slot :name="`cell-${column}`" v-bind="slotProps" />
        </template>
      </AppTable>
    </div>

    <AppModal :open="modalOpen" :title="modalTitle" @close="closeModal">
      <component
        v-if="customFormComponent"
        :is="customFormComponent"
        v-model="formState"
        v-bind="customFormProps"
      />
      <div v-else class="form-grid">
        <template v-for="field in fields" :key="field.key">
          <AppInput
            v-if="field.type === 'text' || field.type === 'password' || field.type === 'date' || field.type === 'number'"
            v-model="formState[field.key]"
            :label="field.label"
            :type="field.type === 'text' ? 'text' : field.type"
          />
          <AppTextarea
            v-else-if="field.type === 'textarea'"
            v-model="formState[field.key]"
            :label="field.label"
          />
          <AppSelect
            v-else-if="field.type === 'select'"
            v-model="formState[field.key]"
            :label="field.label"
            :options="resolveOptions(field)"
          />
          <AppSelect
            v-else-if="field.type === 'boolean'"
            v-model="formState[field.key]"
            :label="field.label"
            :options="booleanOptions"
          />
        </template>
      </div>
      <div v-if="submitError" class="form-submit-error">{{ submitError }}</div>
      <div class="toolbar-row" style="margin-top: 16px;">
        <AppButton @click="submit">{{ resolvedSaveLabel }}</AppButton>
        <AppButton variant="secondary" @click="closeModal">{{ cancelLabel }}</AppButton>
      </div>
    </AppModal>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from "vue";
import { useI18n } from "vue-i18n";

import AppButton from "./AppButton.vue";
import AppEmptyState from "./AppEmptyState.vue";
import AppInput from "./AppInput.vue";
import AppLoader from "./AppLoader.vue";
import AppModal from "./AppModal.vue";
import AppPageHeader from "./AppPageHeader.vue";
import AppSelect from "./AppSelect.vue";
import AppTable from "./AppTable.vue";
import AppTextarea from "./AppTextarea.vue";
import { normalizeApiError } from "@/utils/apiErrors";

const props = defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: "" },
  columns: { type: Array, default: () => [] },
  fields: { type: Array, default: () => [] },
  filters: { type: Array, default: () => [] },
  listFn: { type: Function, required: true },
  createFn: { type: Function, default: null },
  updateFn: { type: Function, default: null },
  initialForm: { type: Object, default: () => ({}) },
  canCreate: { type: Boolean, default: false },
  canEdit: { type: Boolean, default: false },
  createLabel: { type: String, default: "" },
  saveLabel: { type: String, default: "" },
  customFormComponent: { type: [Object, Function], default: null },
  customFormProps: { type: Object, default: () => ({}) },
  customCellKeys: { type: Array, default: () => [] },
});

const emit = defineEmits(["loaded"]);
const { t } = useI18n();

const emptyTitle = computed(() => t("common.empty"));
const cancelLabel = computed(() => t("actions.cancel"));
const resolvedCreateLabel = computed(() => props.createLabel || t("actions.create"));
const resolvedSaveLabel = computed(() => props.saveLabel || t("actions.save"));

const loading = ref(false);
const rows = ref([]);
const modalOpen = ref(false);
const editingRow = ref(null);
const submitError = ref("");
const successMessage = ref("");
const formState = reactive({});
const filterState = reactive({});

const booleanOptions = computed(() => [
  { value: true, label: t("common.active") },
  { value: false, label: t("common.inactive") },
]);

const componentMap = {
  AppInput,
  AppSelect,
  AppTextarea,
};

const modalTitle = computed(() =>
  editingRow.value ? t("actions.edit") : t("actions.create"),
);

const filteredRows = computed(() => {
  return rows.value.filter((row) =>
    props.filters.every((filter) => {
      const value = filterState[filter.key];
      if (value === "" || value === null || value === undefined) return true;
      if (filter.match) return filter.match(row, value);
      return String(row[filter.key] ?? "") === String(value);
    }),
  );
});

function resetForm(source = props.initialForm) {
  Object.keys(formState).forEach((key) => delete formState[key]);
  Object.entries(props.initialForm).forEach(([key, value]) => {
    formState[key] = value;
  });
  Object.entries(source).forEach(([key, value]) => {
    if (Object.prototype.hasOwnProperty.call(formState, key)) {
      formState[key] = value;
    }
  });
}

function resolveOptions(field) {
  if (typeof field.options === "function") {
    return field.options();
  }
  return field.options || [];
}

function resolveComponent(name) {
  return componentMap[name] || AppInput;
}

async function loadRows() {
  loading.value = true;
  try {
    const response = await props.listFn();
    rows.value = Array.isArray(response.data) ? response.data : response.data.results || [];
    emit("loaded", rows.value);
  } finally {
    loading.value = false;
  }
}

function openCreate() {
  editingRow.value = null;
  submitError.value = "";
  successMessage.value = "";
  resetForm();
  modalOpen.value = true;
}

function closeModal() {
  modalOpen.value = false;
  editingRow.value = null;
  submitError.value = "";
}

async function submit() {
  const allowedKeys = Object.keys(props.initialForm);
  const payload = Object.fromEntries(allowedKeys.map((key) => [key, formState[key]]));
  submitError.value = "";
  successMessage.value = "";
  try {
    if (editingRow.value && props.updateFn) {
      await props.updateFn(editingRow.value.id, payload);
    } else if (props.createFn) {
      await props.createFn(payload);
    }
  } catch (error) {
    submitError.value = normalizeApiError(error, {
      fallbackMessage: t("common.saveFailed"),
      t,
    });
    return;
  }
  closeModal();
  await loadRows();
  successMessage.value = t("common.saved");
}

function startEdit(row) {
  if (!props.canEdit) return;
  editingRow.value = row;
  submitError.value = "";
  successMessage.value = "";
  resetForm(row);
  modalOpen.value = true;
}

defineExpose({
  loadRows,
  startEdit,
});

onMounted(() => {
  props.filters.forEach((filter) => {
    filterState[filter.key] = filter.initial ?? "";
  });
  resetForm();
  loadRows();
});
</script>

<style scoped>
.form-submit-error {
  margin-top: 12px;
  color: var(--danger);
  font-size: 14px;
  line-height: 1.4;
}
</style>
