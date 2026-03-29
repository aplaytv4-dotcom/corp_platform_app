export const assignmentFilters = [
  {
    key: "current",
    label: "Current only",
    component: "AppSelect",
    options: [
      { value: "true", label: "Current" },
      { value: "false", label: "Closed" },
    ],
    match: (row, value) => String(row.is_current) === String(value === "true"),
  },
];
