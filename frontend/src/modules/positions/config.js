export const positionsConfig = {
  columns: [
    { key: "name", labelKey: "positions.name" },
    { key: "short_name", labelKey: "positions.shortName" },
    { key: "hierarchy_order", labelKey: "positions.tariffGrade" },
    { key: "is_active", labelKey: "positions.isActive" },
  ],
  fields: [
    { key: "name", labelKey: "positions.name", type: "text" },
    { key: "short_name", labelKey: "positions.shortName", type: "text" },
    { key: "hierarchy_order", labelKey: "positions.tariffGrade", type: "number" },
    { key: "is_active", labelKey: "positions.isActive", type: "boolean" },
  ],
  initialForm: {
    name: "",
    short_name: "",
    hierarchy_order: "",
    is_active: true,
  },
};
