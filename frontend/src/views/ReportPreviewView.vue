<template>
  <div class="page-shell">
    <div class="page-card page-section">
      <AppPageHeader :title="t('reports.title')" />
      <ReportToolbar
        @back="$router.back()"
        @download-word="downloadWord"
        @download-pdf="downloadPdf"
        @print="printReport"
      />
    </div>
    <div class="page-card page-section">
      <iframe v-if="htmlContent" ref="frameRef" class="report-frame" :srcdoc="htmlContent" />
      <AppLoader v-else :label="t('common.loading')" />
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { useI18n } from "vue-i18n";

import { reportsApi } from "@/api/reportsApi";
import AppLoader from "@/components/AppLoader.vue";
import AppPageHeader from "@/components/AppPageHeader.vue";
import ReportToolbar from "@/components/ReportToolbar.vue";

const { t, locale } = useI18n();
const route = useRoute();
const htmlContent = ref("");
const frameRef = ref(null);

const isDaily = computed(() => route.query.type !== "summary");

function buildParams() {
  const lang = locale.value || localStorage.getItem("ui.language") || "ru";
  if (isDaily.value) {
    return { sheet_id: route.query.sheet_id, lang };
  }
  return {
    start_date: route.query.start_date,
    end_date: route.query.end_date,
    lang,
  };
}

async function loadPreview() {
  htmlContent.value = "";
  const params = buildParams();
  const response = isDaily.value ? await reportsApi.dailyHtml(params) : await reportsApi.summaryHtml(params);
  htmlContent.value = response.data;
}

async function downloadBlob(request, filename) {
  const response = await request(buildParams());
  const url = URL.createObjectURL(new Blob([response.data], { type: response.headers["content-type"] }));
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function downloadWord() {
  return downloadBlob(isDaily.value ? reportsApi.dailyWord : reportsApi.summaryWord, isDaily.value ? "daily-report.docx" : "summary-report.docx");
}

function downloadPdf() {
  return downloadBlob(isDaily.value ? reportsApi.dailyPdf : reportsApi.summaryPdf, isDaily.value ? "daily-report.pdf" : "summary-report.pdf");
}

function printReport() {
  frameRef.value?.contentWindow?.print();
}

watch(
  [() => locale.value, () => route.fullPath],
  loadPreview,
  { immediate: true },
);
</script>

<style scoped>
.report-frame {
  width: 100%;
  min-height: 72vh;
  border: 1px solid var(--border);
  border-radius: 14px;
  background: white;
}
</style>
