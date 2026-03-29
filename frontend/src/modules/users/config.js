export function useUsersConfig(referenceStore) {
  return {
    columns: [
      { key: "username", label: "Login" },
      { key: "full_name", label: "Full name" },
      { key: "role", label: "Role" },
      { key: "scope_type", label: "Scope" },
      { key: "management_name", label: "Management" },
      { key: "department_name", label: "Department" },
      { key: "is_active", label: "Active" },
    ],
    fields: [
      { key: "username", label: "Username", type: "text" },
      { key: "password", label: "Password", type: "password" },
      { key: "full_name", label: "Full name", type: "text" },
      { key: "role", label: "Role", type: "select", options: [{ value: "admin", label: "admin" }, { value: "manager", label: "manager" }] },
      { key: "scope_type", label: "Scope type", type: "select", options: [{ value: "all", label: "all" }, { value: "management", label: "management" }, { value: "department", label: "department" }] },
      { key: "management", label: "Management", type: "select", options: () => referenceStore.managements.map((item) => ({ value: item.id, label: item.name })) },
      { key: "department", label: "Department", type: "select", options: () => referenceStore.departments.map((item) => ({ value: item.id, label: item.name })) },
      { key: "is_active", label: "Active", type: "boolean" },
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
