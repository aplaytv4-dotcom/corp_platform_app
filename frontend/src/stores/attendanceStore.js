import { defineStore } from "pinia";

import { attendanceApi } from "@/api/attendanceApi";
import { todayIso } from "@/utils/date";

export const useAttendanceStore = defineStore("attendance", {
  state: () => ({
    selectedDate: todayIso(),
    selectedDepartment: "",
    currentSheet: null,
    items: [],
    loading: false,
    saving: false,
  }),
  actions: {
    reset() {
      this.currentSheet = null;
      this.items = [];
    },
    async openOrCreateSheet() {
      this.loading = true;
      try {
        const payload = {
          date: this.selectedDate,
          department: this.selectedDepartment,
        };
        const { data } = await attendanceApi.openOrCreate(payload);
        this.currentSheet = data;
        this.items = (data.items || []).map((item) => ({
          ...item,
          status: item.status || "present",
          absence_reason: item.absence_reason || null,
          note: item.note || "",
        }));
        return data;
      } finally {
        this.loading = false;
      }
    },
    async saveSheet() {
      if (!this.currentSheet?.id) return null;
      this.saving = true;
      try {
        const payload = {
          items: this.items.map((item) => ({
            employee_id: item.employee,
            status: item.status,
            absence_reason: item.absence_reason || null,
            note: item.note || "",
          })),
        };
        const { data } = await attendanceApi.bulkUpdate(this.currentSheet.id, payload);
        this.currentSheet = data;
        this.items = data.items || [];
        return data;
      } finally {
        this.saving = false;
      }
    },
  },
});
