export function useStaffUnitsConfig(referenceStore) {
  return {
    columns: [
      { key: "department_name", labelKey: "staffUnits.department" },
      { key: "staff_position_name", labelKey: "staffUnits.staffPosition" },
      { key: "unit_number", labelKey: "staffUnits.unitNumber" },
      { key: "is_active", labelKey: "staffUnits.isActive" },
    ],
    fields: [
      {
        key: "department",
        labelKey: "staffUnits.department",
        type: "select",
        options: () => referenceStore.departments.map((item) => ({ value: item.id, label: item.name })),
      },
      {
        key: "staff_position",
        labelKey: "staffUnits.staffPosition",
        type: "select",
        options: () => referenceStore.positions.map((item) => ({ value: item.id, label: item.name })),
      },
      { key: "unit_number", labelKey: "staffUnits.unitNumber", type: "text" },
      { key: "is_active", labelKey: "staffUnits.isActive", type: "boolean" },
    ],
    initialForm: {
      department: "",
      staff_position: "",
      unit_number: "",
      is_active: true,
    },
  };
}
