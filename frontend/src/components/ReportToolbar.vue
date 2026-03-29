<template>
  <div class="toolbar-row">
    <AppButton variant="secondary" @click="$emit('back')">{{ t("actions.back") }}</AppButton>
    <AppButton @click="$emit('download-word')">{{ t("actions.saveWord") }}</AppButton>
    <AppButton @click="$emit('download-pdf')">{{ t("actions.savePdf") }}</AppButton>
    <AppButton variant="secondary" @click="$emit('print')">{{ t("actions.print") }}</AppButton>
  </div>
</template>

<script setup>
import { useI18n } from "vue-i18n";

import AppButton from "./AppButton.vue";

defineEmits(["back", "download-word", "download-pdf", "print"]);

const { t } = useI18n();
</script>
