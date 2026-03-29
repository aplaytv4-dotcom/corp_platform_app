import http from "./http";

export const reportsApi = {
  dailyHtml(params) {
    return http.get("/api/reports/daily-attendance-html/", { params, responseType: "text" });
  },
  dailyWord(params) {
    return http.get("/api/reports/daily-attendance-word/", { params, responseType: "blob" });
  },
  dailyPdf(params) {
    return http.get("/api/reports/daily-attendance-pdf/", { params, responseType: "blob" });
  },
  summaryHtml(params) {
    return http.get("/api/reports/summary-html/", { params, responseType: "text" });
  },
  summaryWord(params) {
    return http.get("/api/reports/summary-word/", { params, responseType: "blob" });
  },
  summaryPdf(params) {
    return http.get("/api/reports/summary-pdf/", { params, responseType: "blob" });
  },
};
