import { defineStore } from "pinia";

import { absenceReasonsApi } from "@/api/absenceReasonsApi";
import { departmentsApi } from "@/api/departmentsApi";
import { managementsApi } from "@/api/managementsApi";
import { positionsApi } from "@/api/positionsApi";

export const useReferenceStore = defineStore("reference", {
  state: () => ({
    departments: [],
    positions: [],
    absenceReasons: [],
    managements: [],
    loading: false,
  }),
  actions: {
    async loadDepartments(params) {
      const { data } = await departmentsApi.list(params);
      this.departments = Array.isArray(data) ? data : data.results || [];
      return this.departments;
    },
    async loadPositions(params) {
      const { data } = await positionsApi.list(params);
      this.positions = Array.isArray(data) ? data : data.results || [];
      return this.positions;
    },
    async loadAbsenceReasons(params) {
      const { data } = await absenceReasonsApi.list(params);
      this.absenceReasons = Array.isArray(data) ? data : data.results || [];
      return this.absenceReasons;
    },
    async loadManagements(params) {
      const { data } = await managementsApi.list(params);
      this.managements = Array.isArray(data) ? data : data.results || [];
      return this.managements;
    },
  },
});
