export const positionsConfig = {
  columns: [
    { key: "name", label: "Name" },
    { key: "short_name", label: "Short name" },
    { key: "is_active", label: "Active" },
  ],
  fields: [
    { key: "name", label: "Name", type: "text" },
    { key: "short_name", label: "Short name", type: "text" },
    { key: "is_active", label: "Active", type: "boolean" },
  ],
  initialForm: {
    name: "",
    short_name: "",
    is_active: true,
  },
};
