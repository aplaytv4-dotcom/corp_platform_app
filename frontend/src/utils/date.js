export function todayIso() {
  return new Date().toISOString().slice(0, 10);
}

export function formatDate(value) {
  if (!value) return "";
  return new Date(value).toLocaleDateString();
}
