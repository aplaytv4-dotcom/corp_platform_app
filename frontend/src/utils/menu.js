export function buildMenu({ t, isAdmin }) {
  const items = [
    { to: "/attendance", label: t("menu.attendance") },
    { to: "/employees", label: t("menu.employees") },
    { to: "/absence-reasons", label: t("menu.absenceReasons") },
  ];

  if (isAdmin) {
    items.push(
      { to: "/users", label: t("menu.users") },
      { to: "/managements", label: t("menu.managements") },
      { to: "/departments", label: t("menu.departments") },
      { to: "/positions", label: t("menu.positions") },
      { to: "/staff-units", label: t("menu.staffUnits") },
      { to: "/assignments", label: t("menu.assignments") },
    );
  }

  return items;
}
