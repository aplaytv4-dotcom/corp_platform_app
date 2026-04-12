function stringifyValue(value) {
  if (value == null) return "";
  if (typeof value === "string" || typeof value === "number" || typeof value === "boolean") {
    return String(value);
  }
  return "";
}

function buildRowLabel(index, t) {
  const rowLabel = typeof t === "function" ? t("common.row") : "Row";
  return `${rowLabel} ${index + 1}`;
}

function flattenErrorValue(value, { t, path = "" } = {}) {
  const textValue = stringifyValue(value);
  if (textValue) {
    return path ? `${path}: ${textValue}` : textValue;
  }

  if (Array.isArray(value)) {
    return value
      .map((item, index) => {
        const nextPath = path === "items" ? buildRowLabel(index, t) : path;
        return flattenErrorValue(item, { t, path: nextPath });
      })
      .filter(Boolean)
      .join(" | ");
  }

  if (typeof value === "object") {
    return Object.entries(value)
      .map(([key, item]) => {
        const nextPath = key === "detail"
          ? path
          : path
            ? `${path}.${key}`
            : key;
        return flattenErrorValue(item, { t, path: nextPath });
      })
      .filter(Boolean)
      .join(" | ");
  }

  return "";
}

export function normalizeApiError(error, { fallbackMessage = "Operation failed", t } = {}) {
  const data = error?.response?.data;
  const message = flattenErrorValue(data, { t }) || error?.message || "";
  return message || fallbackMessage;
}
