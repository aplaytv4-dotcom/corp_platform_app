export function useUsersConfig(referenceStore) {
  return {
    columns: [
      { key: "username", labelKey: "users.username" },
      { key: "full_name", labelKey: "users.fullName" },
      { key: "role", labelKey: "users.role" },
      { key: "scope_type", labelKey: "users.scope" },
      { key: "management_name", labelKey: "users.management" },
      { key: "department_name", labelKey: "users.department" },
      { key: "is_active", labelKey: "users.isActive" },
    ],
    fields: [
      { key: "username", labelKey: "users.username", type: "text" },
      { key: "password", labelKey: "users.password", type: "password" },
      { key: "full_name", labelKey: "users.fullName", type: "text" },
      { key: "role", labelKey: "users.role", type: "select", options: [{ value: "admin", labelKey: "users.admin" }, { value: "manager", labelKey: "users.manager" }] },
      { key: "scope_type", labelKey: "users.scopeType", type: "select", options: [{ value: "all", labelKey: "users.scopeAll" }, { value: "management", labelKey: "users.scopeManagement" }, { value: "department", labelKey: "users.scopeDepartment" }] },
      { key: "management", labelKey: "users.management", type: "select", options: () => referenceStore.managements.map((item) => ({ value: item.id, label: item.name })) },
      { key: "department", labelKey: "users.department", type: "select", options: () => referenceStore.departments.map((item) => ({ value: item.id, label: item.name })) },
      { key: "is_active", labelKey: "users.isActive", type: "boolean" },
    ],
    initialForm: {
      username: "",
      password: "",
      full_name: "",
      role: "manager",
      scope_type: "department",
      management: "",
      department: "",
      is_active: true,
    },
  };
}
