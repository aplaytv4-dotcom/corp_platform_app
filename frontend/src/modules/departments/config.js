export function useDepartmentsConfig(referenceStore) {
  return {
    columns: [
      { key: "management_name", labelKey: "departments.management" },
      { key: "name", labelKey: "departments.name" },
      { key: "code", labelKey: "departments.code" },
      { key: "is_active", labelKey: "departments.isActive" },
    ],
    fields: [
      { key: "management", labelKey: "departments.management", type: "select", options: () => referenceStore.managements.map((item) => ({ value: item.id, label: item.name })) },
      { key: "name", labelKey: "departments.name", type: "text" },
      { key: "code", labelKey: "departments.code", type: "text" },
      { key: "is_active", labelKey: "departments.isActive", type: "boolean" },
    ],
    initialForm: {
      management: "",
      name: "",
      code: "",
      is_active: true,
    },
  };
}
