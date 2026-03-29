export function useStaffUnitsConfig(referenceStore) {
  return {
    columns: [
      { key: "department_name", label: "Department" },
      { key: "staff_position_name", label: "Staff position" },
      { key: "unit_number", label: "Unit number" },
      { key: "is_active", label: "Active" },
    ],
    fields: [
      { key: "department", label: "Department", type: "select", options: () => referenceStore.departments.map((item) => ({ value: item.id, label: item.name })) },
      { key: "staff_position", label: "Staff position", type: "select", options: () => referenceStore.positions.map((item) => ({ value: item.id, label: item.name })) },
      { key: "unit_number", label: "Unit number", type: "text" },
      { key: "is_active", label: "Active", type: "boolean" },
    ],
    initialForm: {
      department: "",
      staff_position: "",
      unit_number: "",
      is_active: true,
    },
  };
}
