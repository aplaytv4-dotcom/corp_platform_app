export const assignmentFilters = [
  {
    key: "current",
    labelKey: "assignments.currentOnly",
    component: "AppSelect",
    options: [
      { value: "true", labelKey: "assignments.current" },
      { value: "false", labelKey: "assignments.closed" },
    ],
    match: (row, value) => String(row.is_current) === String(value === "true"),
  },
];
