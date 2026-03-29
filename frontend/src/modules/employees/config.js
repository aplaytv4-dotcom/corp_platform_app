export const employeeFilters = [
  {
    key: "search",
    label: "Search",
    component: "AppInput",
    match: (row, value) =>
      [row.last_name, row.first_name, row.middle_name, row.short_fio, row.personnel_number]
        .join(" ")
        .toLowerCase()
        .includes(String(value).toLowerCase()),
  },
];
