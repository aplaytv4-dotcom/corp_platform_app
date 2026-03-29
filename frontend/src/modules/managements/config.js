export const managementsConfig = {
  columns: [
    { key: "name", labelKey: "managements.name" },
    { key: "code", labelKey: "managements.code" },
    { key: "is_active", labelKey: "managements.isActive" },
  ],
  fields: [
    { key: "name", labelKey: "managements.name", type: "text" },
    { key: "code", labelKey: "managements.code", type: "text" },
    { key: "is_active", labelKey: "managements.isActive", type: "boolean" },
  ],
  initialForm: {
    name: "",
    code: "",
    is_active: true,
  },
};
