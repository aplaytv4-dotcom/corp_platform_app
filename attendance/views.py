from datetime import date

from django.http import Http404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from attendance.models import AbsenceReason
from attendance.permissions import IsAdmin
from attendance.selectors import (
    build_daily_report_data,
    build_summary_report_data,
    get_absence_reasons_queryset,
    get_attendance_sheets_for_user,
    get_sheet_or_none_for_user,
)
from attendance.serializers import (
    AbsenceReasonCreateSerializer,
    AbsenceReasonListSerializer,
    AbsenceReasonUpdateSerializer,
    AttendanceSheetDetailSerializer,
    BulkUpdateAttendanceSerializer,
    OpenAttendanceSheetSerializer,
)
from common.permissions import user_has_department_access
from common.services import attachment_response, build_rtf_document, build_simple_pdf, html_response


class AbsenceReasonViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = AbsenceReason.objects.filter(is_active=True)

    def get_permissions(self):
        if self.action in {"update", "partial_update", "destroy"}:
            return [IsAuthenticated(), IsAdmin()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create":
            return AbsenceReasonCreateSerializer
        if self.action in {"update", "partial_update"}:
            return AbsenceReasonUpdateSerializer
        return AbsenceReasonListSerializer

    def get_queryset(self):
        return get_absence_reasons_queryset()


class AttendanceSheetViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_attendance_sheets_for_user(self.request.user).prefetch_related("items", "items__employee", "items__absence_reason")

    def retrieve(self, request, pk=None):
        instance = self.get_queryset().filter(pk=pk).first()
        if not instance:
            raise Http404
        return Response(AttendanceSheetDetailSerializer(instance).data)

    @action(detail=False, methods=["post"], url_path="open-or-create")
    def open_or_create(self, request):
        serializer = OpenAttendanceSheetSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        department = serializer.validated_data["department"]
        if not user_has_department_access(request.user, department):
            raise PermissionDenied("No access to selected department.")
        sheet = serializer.save()
        return Response(AttendanceSheetDetailSerializer(sheet).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["patch"], url_path="bulk-update")
    def bulk_update(self, request, pk=None):
        sheet = get_sheet_or_none_for_user(request.user, pk)
        if not sheet:
            raise Http404
        serializer = BulkUpdateAttendanceSerializer(data=request.data, context={"request": request, "sheet_id": sheet.id})
        serializer.is_valid(raise_exception=True)
        updated_sheet = serializer.save()
        return Response(AttendanceSheetDetailSerializer(updated_sheet).data)


class DailyAttendanceHtmlReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get_sheet(self, request):
        sheet_id = request.GET.get("sheet_id")
        if not sheet_id:
            raise Http404
        sheet = get_sheet_or_none_for_user(request.user, sheet_id)
        if not sheet:
            raise Http404
        return sheet

    def get(self, request):
        sheet = self.get_sheet(request)
        data = build_daily_report_data(sheet)
        rows = "".join(
            f"<tr><td>{row['employee']}</td><td>{row['personnel_number']}</td><td>{row['status']}</td><td>{row['absence_reason']}</td><td>{row['note']}</td></tr>"
            for row in data["rows"]
        )
        body = (
            f"<h1>Daily attendance</h1><p>Date: {data['date']}</p><p>Department: {data['department']}</p>"
            "<table><thead><tr><th>Employee</th><th>Personnel #</th><th>Status</th><th>Reason</th><th>Note</th></tr></thead>"
            f"<tbody>{rows}</tbody></table>"
        )
        return html_response("Daily attendance", body)


class DailyAttendanceWordReportView(DailyAttendanceHtmlReportView):
    def get(self, request):
        sheet = self.get_sheet(request)
        data = build_daily_report_data(sheet)
        lines = [
            f"{row['employee']} | {row['personnel_number']} | {row['status']} | {row['absence_reason']} | {row['note']}"
            for row in data["rows"]
        ]
        content = build_rtf_document("Daily attendance", lines)
        return attachment_response(content, "daily-attendance.rtf", "application/rtf")


class DailyAttendancePdfReportView(DailyAttendanceHtmlReportView):
    def get(self, request):
        sheet = self.get_sheet(request)
        data = build_daily_report_data(sheet)
        lines = [
            f"{row['employee']} | {row['personnel_number']} | {row['status']} | {row['absence_reason']} | {row['note']}"
            for row in data["rows"]
        ]
        content = build_simple_pdf("Daily attendance", lines)
        return attachment_response(content, "daily-attendance.pdf", "application/pdf")


class SummaryHtmlReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get_data(self, request):
        start_date = date.fromisoformat(request.GET["start_date"])
        end_date = date.fromisoformat(request.GET["end_date"])
        return build_summary_report_data(request.user, start_date, end_date)

    def get(self, request):
        data = self.get_data(request)
        rows = "".join(
            f"<tr><td>{row['department__name']}</td><td>{row['present_count']}</td><td>{row['absent_count']}</td></tr>"
            for row in data["rows"]
        )
        body = (
            f"<h1>Summary attendance</h1><p>Period: {data['start_date']} - {data['end_date']}</p>"
            "<table><thead><tr><th>Department</th><th>Present</th><th>Absent</th></tr></thead>"
            f"<tbody>{rows}</tbody></table>"
        )
        return html_response("Summary attendance", body)


class SummaryWordReportView(SummaryHtmlReportView):
    def get(self, request):
        data = self.get_data(request)
        lines = [f"{row['department__name']} | present={row['present_count']} | absent={row['absent_count']}" for row in data["rows"]]
        content = build_rtf_document("Summary attendance", lines)
        return attachment_response(content, "summary-attendance.rtf", "application/rtf")


class SummaryPdfReportView(SummaryHtmlReportView):
    def get(self, request):
        data = self.get_data(request)
        lines = [f"{row['department__name']} | present={row['present_count']} | absent={row['absent_count']}" for row in data["rows"]]
        content = build_simple_pdf("Summary attendance", lines)
        return attachment_response(content, "summary-attendance.pdf", "application/pdf")
