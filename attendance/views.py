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
from common.services import attachment_response, build_pdf_document, build_word_document, html_response
from staff.selectors import get_assignments_for_department_on_date


REPORT_LABELS = {
    "ru": {
        "daily_title": "\u0415\u0436\u0435\u0434\u043d\u0435\u0432\u043d\u044b\u0439 \u043e\u0442\u0447\u0435\u0442 \u043f\u043e \u043f\u043e\u0441\u0435\u0449\u0430\u0435\u043c\u043e\u0441\u0442\u0438",
        "summary_title": "\u0421\u0432\u043e\u0434\u043d\u044b\u0439 \u043e\u0442\u0447\u0435\u0442 \u043f\u043e \u043f\u043e\u0441\u0435\u0449\u0430\u0435\u043c\u043e\u0441\u0442\u0438",
        "row_number": "\u2116",
        "date": "\u0414\u0430\u0442\u0430",
        "department": "\u041e\u0442\u0434\u0435\u043b",
        "period": "\u041f\u0435\u0440\u0438\u043e\u0434",
        "employee": "\u0421\u043e\u0442\u0440\u0443\u0434\u043d\u0438\u043a",
        "position": "\u0424\u0430\u043a\u0442\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u0434\u043e\u043b\u0436\u043d\u043e\u0441\u0442\u044c",
        "status": "\u0421\u0442\u0430\u0442\u0443\u0441",
        "reason": "\u041f\u0440\u0438\u0447\u0438\u043d\u0430",
        "note": "\u041f\u0440\u0438\u043c\u0435\u0447\u0430\u043d\u0438\u0435",
        "present": "\u041f\u0440\u0438\u0441\u0443\u0442\u0441\u0442\u0432\u0443\u0435\u0442",
        "absent": "\u041e\u0442\u0441\u0443\u0442\u0441\u0442\u0432\u0443\u0435\u0442",
        "present_count": "\u041f\u0440\u0438\u0441\u0443\u0442\u0441\u0442\u0432\u0443\u0435\u0442",
        "absent_count": "\u041e\u0442\u0441\u0443\u0442\u0441\u0442\u0432\u0443\u0435\u0442",
        "no_reason": "-",
        "no_note": "-",
        "department_head": "\u041d\u0430\u0447\u0430\u043b\u044c\u043d\u0438\u043a \u043e\u0442\u0434\u0435\u043b\u0430",
        "signature_hint": "(\u043f\u043e\u0434\u043f\u0438\u0441\u044c)",
        "name_hint": "(\u0424.\u0418.\u041e.)",
        "date_hint": "(\u0434\u0430\u0442\u0430)",
        "generated_at": "\u0414\u0430\u0442\u0430 \u0444\u043e\u0440\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f \u043e\u0442\u0447\u0435\u0442\u0430",
        "for_date": "\u0437\u0430",
        "not_assigned": "\u043d\u0435 \u043d\u0430\u0437\u043d\u0430\u0447\u0435\u043d",
        "staff_total": "\u041f\u043e \u0448\u0442\u0430\u0442\u0443",
        "present_total": "\u041f\u0440\u0438\u0441\u0443\u0442\u0441\u0442\u0432\u0443\u044e\u0442",
        "absent_total": "\u041e\u0442\u0441\u0443\u0442\u0441\u0442\u0432\u0443\u044e\u0442",
        "absent_reasons": "\u041f\u0440\u0438\u0447\u0438\u043d\u044b \u043e\u0442\u0441\u0443\u0442\u0441\u0442\u0432\u0438\u044f",
        "none": "\u041d\u0435\u0442",
        "people": "\u0447\u0435\u043b\u043e\u0432\u0435\u043a",
    },
    "uz": {
        "daily_title": "Kunlik davomat hisoboti",
        "summary_title": "Umumiy davomat hisoboti",
        "row_number": "\u2116",
        "date": "Sana",
        "department": "Bo'lim",
        "period": "Davr",
        "employee": "Xodim",
        "position": "Amaldagi lavozim",
        "status": "Holat",
        "reason": "Sabab",
        "note": "Izoh",
        "present": "Bor",
        "absent": "Yo'q",
        "present_count": "Bor",
        "absent_count": "Yo'q",
        "no_reason": "-",
        "no_note": "-",
        "department_head": "Bo'lim boshlig'i",
        "signature_hint": "(imzo)",
        "name_hint": "(F.I.Sh.)",
        "date_hint": "(sana)",
        "generated_at": "Hisobot tuzilgan sana",
        "for_date": "uchun",
        "not_assigned": "tayinlanmagan",
        "staff_total": "Shtat bo'yicha",
        "present_total": "Ishda bo'lganlar",
        "absent_total": "Yo'q bo'lganlar",
        "absent_reasons": "Yo'qlik sabablari",
        "none": "Yo'q",
        "people": "nafar",
    },
}


def get_report_labels(request):
    lang = (request.GET.get("lang") or "ru").lower()
    if lang not in REPORT_LABELS:
        lang = "ru"
    return REPORT_LABELS[lang]


def get_report_lang(request):
    lang = (request.GET.get("lang") or "ru").lower()
    return lang if lang in REPORT_LABELS else "ru"


def localize_status(status_value, labels):
    if status_value == "present":
        return labels["present"]
    if status_value == "absent":
        return labels["absent"]
    return status_value


def format_report_date(value, lang):
    if isinstance(value, str):
        value = date.fromisoformat(value)

    month_names = {
        "ru": [
            "\u044f\u043d\u0432\u0430\u0440\u044f",
            "\u0444\u0435\u0432\u0440\u0430\u043b\u044f",
            "\u043c\u0430\u0440\u0442\u0430",
            "\u0430\u043f\u0440\u0435\u043b\u044f",
            "\u043c\u0430\u044f",
            "\u0438\u044e\u043d\u044f",
            "\u0438\u044e\u043b\u044f",
            "\u0430\u0432\u0433\u0443\u0441\u0442\u0430",
            "\u0441\u0435\u043d\u0442\u044f\u0431\u0440\u044f",
            "\u043e\u043a\u0442\u044f\u0431\u0440\u044f",
            "\u043d\u043e\u044f\u0431\u0440\u044f",
            "\u0434\u0435\u043a\u0430\u0431\u0440\u044f",
        ],
        "uz": [
            "yanvar",
            "fevral",
            "mart",
            "aprel",
            "may",
            "iyun",
            "iyul",
            "avgust",
            "sentyabr",
            "oktyabr",
            "noyabr",
            "dekabr",
        ],
    }

    if lang == "uz":
        return f"{value.day} {month_names['uz'][value.month - 1]} {value.year} yil"
    return f"{value.day} {month_names['ru'][value.month - 1]} {value.year} \u0433\u043e\u0434\u0430"


def build_daily_report_columns(rows, labels):
    has_reason = any(row["absence_reason"] for row in rows)
    has_note = any(row["note"] for row in rows)

    columns = [
        {"key": "row_number", "label": labels["row_number"]},
        {"key": "employee", "label": labels["employee"]},
        {"key": "actual_position", "label": labels["position"]},
        {"key": "status", "label": labels["status"]},
    ]
    if has_reason:
        columns.append({"key": "absence_reason", "label": labels["reason"]})
    if has_note:
        columns.append({"key": "note", "label": labels["note"]})
    return columns


def build_daily_row_values(row, columns, labels, row_number):
    values = []
    for column in columns:
        key = column["key"]
        if key == "row_number":
            values.append(str(row_number))
        elif key == "status":
            values.append(localize_status(row["status"], labels))
        else:
            values.append(row.get(key) or labels.get(f"no_{key}", "-"))
    return values


def to_short_fio(full_name):
    if not full_name:
        return ""
    parts = [part for part in str(full_name).split() if part]
    if len(parts) <= 1:
        return parts[0] if parts else ""
    last_name = parts[0]
    initials = "".join(f"{part[:1]}." for part in parts[1:] if part[:1])
    return f"{last_name} {initials}".strip()


def get_department_signatory(department, labels, target_date=None, absent_employee_ids=None):
    assignments = list(get_assignments_for_department_on_date(department, target_date or date.today()))
    absent_employee_ids = set(absent_employee_ids or [])
    assignments = [
        assignment
        for assignment in assignments
        if assignment.employee_id not in absent_employee_ids
    ]
    if not assignments:
        return {
            "role": labels["department_head"],
            "name": "",
        }

    def assignment_priority(assignment):
        actual_order = getattr(assignment.actual_position, "hierarchy_order", None)
        staff_order = getattr(assignment.staff_unit.staff_position, "hierarchy_order", None)
        if actual_order is not None:
            return -actual_order
        if staff_order is not None:
            return -staff_order
        return 100000

    chosen = sorted(
        assignments,
        key=lambda assignment: (
            assignment_priority(assignment),
            assignment.staff_unit.unit_number,
            assignment.employee.last_name,
            assignment.employee.first_name,
            assignment.employee.middle_name,
        ),
    )[0]
    chosen_role = (chosen.actual_position.name or "").strip() or labels["department_head"]
    return {
        "role": chosen_role,
        "name": chosen.employee.short_fio or str(chosen.employee),
    }


def build_signature_block(labels, signatory, lang, sign_date=None):
    return {
        "role": signatory["role"],
        "role_hint": "",
        "signature_hint": labels["signature_hint"],
        "name": signatory["name"],
        "name_hint": labels["name_hint"],
        "date": format_report_date(sign_date or date.today(), lang),
        "date_hint": labels["date_hint"],
    }


def build_daily_statistics(rows):
    total_staff = len(rows)
    present_total = sum(1 for row in rows if row["status"] == "present")
    absent_total = sum(1 for row in rows if row["status"] == "absent")
    reason_counts = {}
    reason_employees = {}
    for row in rows:
        if row["status"] == "absent" and row["absence_reason"]:
            reason_counts[row["absence_reason"]] = reason_counts.get(row["absence_reason"], 0) + 1
            reason_employees.setdefault(row["absence_reason"], []).append(row["employee"])
    return {
        "total_staff": total_staff,
        "present_total": present_total,
        "absent_total": absent_total,
        "reason_counts": reason_counts,
        "reason_employees": reason_employees,
    }


def build_daily_summary_html(stats, labels):
    if stats["reason_employees"]:
        items = "".join(
            f"<li><strong>{reason}:</strong> {', '.join(employees)}</li>"
            for reason, employees in stats["reason_employees"].items()
        )
        reasons_html = f"<ul class=\"report-summary-list\">{items}</ul>"
    else:
        reasons_html = f"<p class=\"report-summary-empty\">{labels['none']}</p>"

    return (
        f"<div class=\"report-summary report-summary-left\">"
        f"<p><strong>{labels['staff_total']}:</strong> {stats['total_staff']} {labels['people']}</p>"
        f"<p><strong>{labels['present_total']}:</strong> {stats['present_total']} {labels['people']}</p>"
        f"<p><strong>{labels['absent_total']}:</strong> {stats['absent_total']} {labels['people']}</p>"
        f"<div class=\"report-summary-reasons report-summary-reasons-highlight\">"
        f"{reasons_html}"
        f"</div>"
        f"</div>"
    )


def build_daily_summary_lines(stats, labels):
    lines = [
        f"{labels['staff_total']}: {stats['total_staff']} {labels['people']}",
        f"{labels['present_total']}: {stats['present_total']} {labels['people']}",
        f"{labels['absent_total']}: {stats['absent_total']} {labels['people']}",
    ]
    if stats["reason_employees"]:
        lines.extend(
            f"{reason}: {', '.join(employees)}"
            for reason, employees in stats["reason_employees"].items()
        )
    else:
        lines.append(f"{labels['absent_reasons']}: {labels['none']}")
    return lines


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
        return get_attendance_sheets_for_user(self.request.user).prefetch_related(
            "items",
            "items__employee",
            "items__absence_reason",
        )

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
        serializer = BulkUpdateAttendanceSerializer(
            data=request.data,
            context={"request": request, "sheet_id": sheet.id},
        )
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
        lang = get_report_lang(request)
        labels = get_report_labels(request)
        absent_employee_ids = [row["employee_id"] for row in data["rows"] if row["status"] == "absent"]
        signatory = get_department_signatory(
            sheet.department,
            labels,
            target_date=data["date"],
            absent_employee_ids=absent_employee_ids,
        )
        columns = build_daily_report_columns(data["rows"], labels)
        stats = build_daily_statistics(data["rows"])
        header_html = "".join(
            f"<th class=\"{'col-number' if column['key'] == 'row_number' else ''}\">{column['label']}</th>"
            for column in columns
        )

        row_html = []
        for index, row in enumerate(data["rows"], start=1):
            cells = []
            for column, value in zip(columns, build_daily_row_values(row, columns, labels, index)):
                td_class = " class=\"text-center\"" if column["key"] == "row_number" else ""
                cells.append(f"<td{td_class}>{value}</td>")
            row_html.append(f"<tr>{''.join(cells)}</tr>")

        body = (
            f"<p class=\"report-generated-at\">{labels['generated_at']}: {format_report_date(date.today(), lang)}</p>"
            f"<h1 class=\"report-title\">{labels['daily_title']}<br><span class=\"report-title-subline\">{labels['for_date']} {format_report_date(data['date'], lang)}</span></h1>"
            f"<div class=\"report-meta\">"
            f"<p><strong>{labels['department']}:</strong> {data['department']}</p>"
            f"</div>"
            f"{build_daily_summary_html(stats, labels)}"
            f"<table><thead><tr>{header_html}</tr></thead><tbody>{''.join(row_html)}</tbody></table>"
            f"<div class=\"signature-block\">"
            f"<table class=\"signature-grid\">"
            f"<tr>"
            f"<td class=\"signature-role\">{signatory['role']}</td>"
            f"<td class=\"signature-line\"></td>"
            f"<td class=\"signature-name\">{signatory['name']}</td>"
            f"</tr>"
            f"<tr>"
            f"<td class=\"signature-hint\"></td>"
            f"<td class=\"signature-hint text-center\">{labels['signature_hint']}</td>"
            f"<td class=\"signature-hint text-center\">{labels['name_hint']}</td>"
            f"</tr>"
            f"<tr>"
            f"<td class=\"signature-date-left\">{format_report_date(data['date'], lang)}</td>"
            f"<td></td>"
            f"<td></td>"
            f"</tr>"
            f"<tr>"
            f"<td class=\"signature-hint\">{labels['date_hint']}</td>"
            f"<td></td>"
            f"<td></td>"
            f"</tr>"
            f"</table>"
            f"</div>"
        )
        return html_response(labels["daily_title"], body, lang=lang)


class DailyAttendanceWordReportView(DailyAttendanceHtmlReportView):
    def get(self, request):
        sheet = self.get_sheet(request)
        data = build_daily_report_data(sheet)
        lang = get_report_lang(request)
        labels = get_report_labels(request)
        absent_employee_ids = [row["employee_id"] for row in data["rows"] if row["status"] == "absent"]
        signatory = get_department_signatory(
            sheet.department,
            labels,
            target_date=data["date"],
            absent_employee_ids=absent_employee_ids,
        )
        columns = build_daily_report_columns(data["rows"], labels)
        stats = build_daily_statistics(data["rows"])
        header_html = "".join(
            f"<th class=\"{'col-number' if column['key'] == 'row_number' else ''}\">{column['label']}</th>"
            for column in columns
        )
        row_html = []
        for index, row in enumerate(data["rows"], start=1):
            values = build_daily_row_values(row, columns, labels, index)
            cells = []
            for column, value in zip(columns, values):
                td_class = " class=\"text-center\"" if column["key"] == "row_number" else ""
                cells.append(f"<td{td_class}>{value}</td>")
            row_html.append(f"<tr>{''.join(cells)}</tr>")

        body = (
            f"<p class=\"report-generated-at\">{labels['generated_at']}: {format_report_date(date.today(), lang)}</p>"
            f"<h1 class=\"report-title\">{labels['daily_title']}<br><span class=\"report-title-subline\">{labels['for_date']} {format_report_date(data['date'], lang)}</span></h1>"
            f"<div class=\"report-meta\">"
            f"<p><strong>{labels['department']}:</strong> {data['department']}</p>"
            f"</div>"
            f"{build_daily_summary_html(stats, labels)}"
            f"<table><thead><tr>{header_html}</tr></thead><tbody>{''.join(row_html)}</tbody></table>"
            f"<div class=\"signature-block\">"
            f"<table class=\"signature-grid\">"
            f"<tr>"
            f"<td class=\"signature-role\">{signatory['role']}</td>"
            f"<td class=\"signature-line\"></td>"
            f"<td class=\"signature-name\">{signatory['name']}</td>"
            f"</tr>"
            f"<tr>"
            f"<td class=\"signature-hint\"></td>"
            f"<td class=\"signature-hint text-center\">{labels['signature_hint']}</td>"
            f"<td class=\"signature-hint text-center\">{labels['name_hint']}</td>"
            f"</tr>"
            f"<tr>"
            f"<td class=\"signature-date-left\">{format_report_date(data['date'], lang)}</td>"
            f"<td></td>"
            f"<td></td>"
            f"</tr>"
            f"<tr>"
            f"<td class=\"signature-hint\">{labels['date_hint']}</td>"
            f"<td></td>"
            f"<td></td>"
            f"</tr>"
            f"</table>"
            f"</div>"
        )
        content = build_word_document(labels["daily_title"], body, lang=lang)
        return attachment_response(content, "daily-attendance.doc", "application/msword")


class DailyAttendancePdfReportView(DailyAttendanceHtmlReportView):
    def get(self, request):
        sheet = self.get_sheet(request)
        data = build_daily_report_data(sheet)
        lang = get_report_lang(request)
        labels = get_report_labels(request)
        absent_employee_ids = [row["employee_id"] for row in data["rows"] if row["status"] == "absent"]
        signatory = get_department_signatory(
            sheet.department,
            labels,
            target_date=data["date"],
            absent_employee_ids=absent_employee_ids,
        )
        columns = build_daily_report_columns(data["rows"], labels)
        stats = build_daily_statistics(data["rows"])
        rows = [build_daily_row_values(row, columns, labels, index) for index, row in enumerate(data["rows"], start=1)]
        metadata = [
            f"{labels['generated_at']}: {format_report_date(date.today(), lang)}",
            f"{labels['daily_title']} {labels['for_date']} {format_report_date(data['date'], lang)}",
            f"{labels['department']}: {data['department']}",
            *build_daily_summary_lines(stats, labels),
        ]
        content = build_pdf_document(
            labels["daily_title"],
            metadata,
            [column["label"] for column in columns],
            rows,
            signature_block=build_signature_block(labels, signatory, lang, sign_date=data["date"]),
        )
        return attachment_response(content, "daily-attendance.pdf", "application/pdf")


class SummaryHtmlReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get_data(self, request):
        start_date = date.fromisoformat(request.GET["start_date"])
        end_date = date.fromisoformat(request.GET["end_date"])
        return build_summary_report_data(request.user, start_date, end_date)

    def get(self, request):
        data = self.get_data(request)
        lang = get_report_lang(request)
        labels = get_report_labels(request)
        rows = "".join(
            f"<tr><td>{row['department__name']}</td><td>{row['present_count']}</td><td>{row['absent_count']}</td></tr>"
            for row in data["rows"]
        )
        body = (
            f"<p class=\"report-generated-at\">{labels['generated_at']}: {format_report_date(date.today(), lang)}</p>"
            f"<h1 class=\"report-title\">{labels['summary_title']}</h1>"
            f"<div class=\"report-meta report-meta-centered\">"
            f"<p><strong>{labels['period']}:</strong> {format_report_date(data['start_date'], lang)} - {format_report_date(data['end_date'], lang)}</p>"
            f"</div>"
            f"<table><thead><tr><th>{labels['department']}</th><th>{labels['present_count']}</th><th>{labels['absent_count']}</th></tr></thead>"
            f"<tbody>{rows}</tbody></table>"
        )
        return html_response(labels["summary_title"], body, lang=lang)


class SummaryWordReportView(SummaryHtmlReportView):
    def get(self, request):
        data = self.get_data(request)
        lang = get_report_lang(request)
        labels = get_report_labels(request)
        rows = [
            [row["department__name"], str(row["present_count"]), str(row["absent_count"])]
            for row in data["rows"]
        ]
        body_rows = "".join(
            f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
            for row in rows
        )
        body = (
            f"<p class=\"report-generated-at\">{labels['generated_at']}: {format_report_date(date.today(), lang)}</p>"
            f"<h1 class=\"report-title\">{labels['summary_title']}</h1>"
            f"<div class=\"report-meta report-meta-centered\">"
            f"<p><strong>{labels['period']}:</strong> {format_report_date(data['start_date'], lang)} - {format_report_date(data['end_date'], lang)}</p>"
            f"</div>"
            f"<table><thead><tr><th>{labels['department']}</th><th>{labels['present_count']}</th><th>{labels['absent_count']}</th></tr></thead>"
            f"<tbody>{body_rows}</tbody></table>"
        )
        content = build_word_document(labels["summary_title"], body, lang=lang)
        return attachment_response(content, "summary-attendance.doc", "application/msword")


class SummaryPdfReportView(SummaryHtmlReportView):
    def get(self, request):
        data = self.get_data(request)
        lang = get_report_lang(request)
        labels = get_report_labels(request)
        rows = [
            [row["department__name"], str(row["present_count"]), str(row["absent_count"])]
            for row in data["rows"]
        ]
        metadata = [
            f"{labels['generated_at']}: {format_report_date(date.today(), lang)}",
            f"{labels['period']}: {format_report_date(data['start_date'], lang)} - {format_report_date(data['end_date'], lang)}",
        ]
        content = build_pdf_document(
            labels["summary_title"],
            metadata,
            [labels["department"], labels["present_count"], labels["absent_count"]],
            rows,
        )
        return attachment_response(content, "summary-attendance.pdf", "application/pdf")
