export const managementsConfig = {
  columns: [
    { key: "name", label: "Name" },
    { key: "code", label: "Code" },
    { key: "is_active", label: "Active" },
  ],
  fields: [
    { key: "name", label: "Name", type: "text" },
    { key: "code", label: "Code", type: "text" },
    { key: "is_active", label: "Active", type: "boolean" },
  ],
  initialForm: {
    name: "",
    code: "",
    is_active: true,
  },
};
