export function useDepartmentsConfig(referenceStore) {
  return {
    columns: [
      { key: "management_name", label: "Management" },
      { key: "name", label: "Name" },
      { key: "code", label: "Code" },
      { key: "is_active", label: "Active" },
    ],
    fields: [
      { key: "management", label: "Management", type: "select", options: () => referenceStore.managements.map((item) => ({ value: item.id, label: item.name })) },
      { key: "name", label: "Name", type: "text" },
      { key: "code", label: "Code", type: "text" },
      { key: "is_active", label: "Active", type: "boolean" },
    ],
    initialForm: {
      management: "",
      name: "",
      code: "",
      is_active: true,
    },
  };
}
