from django.urls import include, path
from rest_framework.routers import DefaultRouter

from attendance.views import (
    AbsenceReasonViewSet,
    AttendanceSheetViewSet,
    DailyAttendanceHtmlReportView,
    DailyAttendancePdfReportView,
    DailyAttendanceWordReportView,
    SummaryHtmlReportView,
    SummaryPdfReportView,
    SummaryWordReportView,
)


router = DefaultRouter()
router.register("attendance-sheets", AttendanceSheetViewSet, basename="attendance-sheets")
router.register("absence-reasons", AbsenceReasonViewSet, basename="absence-reasons")


urlpatterns = [
    path("", include(router.urls)),
    path("reports/daily-attendance-html/", DailyAttendanceHtmlReportView.as_view(), name="daily-attendance-html"),
    path("reports/daily-attendance-word/", DailyAttendanceWordReportView.as_view(), name="daily-attendance-word"),
    path("reports/daily-attendance-pdf/", DailyAttendancePdfReportView.as_view(), name="daily-attendance-pdf"),
    path("reports/summary-html/", SummaryHtmlReportView.as_view(), name="summary-html"),
    path("reports/summary-word/", SummaryWordReportView.as_view(), name="summary-word"),
    path("reports/summary-pdf/", SummaryPdfReportView.as_view(), name="summary-pdf"),
]
