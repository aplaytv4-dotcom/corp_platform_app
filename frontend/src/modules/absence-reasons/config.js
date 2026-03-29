export const absenceReasonsConfig = {
  columns: [
    { key: "name", labelKey: "absenceReasons.name" },
    { key: "code", labelKey: "absenceReasons.code" },
    { key: "is_active", labelKey: "absenceReasons.isActive" },
  ],
  fields: [
    { key: "name", labelKey: "absenceReasons.name", type: "text" },
    { key: "code", labelKey: "absenceReasons.code", type: "text" },
    { key: "is_active", labelKey: "absenceReasons.isActive", type: "boolean" },
  ],
  initialForm: {
    name: "",
    code: "",
    is_active: true,
  },
};
