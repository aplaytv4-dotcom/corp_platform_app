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
import { onMounted, ref, watch } from "vue";
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

const isDaily = route.query.type !== "summary";

function buildParams() {
  const lang = locale.value || localStorage.getItem("ui.language") || "ru";
  if (isDaily) {
    return { sheet_id: route.query.sheet_id, lang };
  }
  return {
    start_date: route.query.start_date,
    end_date: route.query.end_date,
    lang,
  };
}

async function loadPreview() {
  const params = buildParams();
  const response = isDaily ? await reportsApi.dailyHtml(params) : await reportsApi.summaryHtml(params);
  htmlContent.value = response.data;
}

async function downloadBlob(request, filename) {
  const response = await request(buildParams());
  const url = URL.createObjectURL(new Blob([response.data], { type: response.headers["content-type"] }));
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}

function downloadWord() {
  return downloadBlob(isDaily ? reportsApi.dailyWord : reportsApi.summaryWord, isDaily ? "daily-report.doc" : "summary-report.doc");
}

function downloadPdf() {
  return downloadBlob(isDaily ? reportsApi.dailyPdf : reportsApi.summaryPdf, isDaily ? "daily-report.pdf" : "summary-report.pdf");
}

function printReport() {
  frameRef.value?.contentWindow?.print();
}

onMounted(loadPreview);
watch(
  () => locale.value,
  () => {
    loadPreview();
  },
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
