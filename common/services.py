from io import BytesIO
from pathlib import Path

from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def build_html_document(title: str, body: str, lang: str = "ru") -> str:
    return f"""<!doctype html>
<html lang="{lang}">
  <head>
    <meta charset="utf-8">
    <title>{title}</title>
    <style>
      @page {{
        size: A4;
        margin: 22mm 16mm 18mm 16mm;
      }}
      body {{
        margin: 0;
        background: #f3f4f6;
        color: #1f2937;
        font-family: "Times New Roman", Times, serif;
        font-size: 14pt;
        line-height: 1.35;
      }}
      .report {{
        max-width: 980px;
        margin: 24px auto;
        background: #ffffff;
        border: 1px solid #d1d5db;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
        padding: 24px 28px 28px;
      }}
      .report-title {{
        margin: 0 0 14px;
        text-align: center;
        font-size: 16pt;
        line-height: 1.3;
        font-weight: 700;
      }}
      .report-title-subline {{
        display: inline-block;
        margin-top: 2px;
        font-weight: 400;
      }}
      .report-generated-at {{
        margin: 0 0 8px;
        text-align: left;
        font-size: 8pt;
        color: #64748b;
      }}
      .report-meta {{
        margin: 0 0 16px;
      }}
      .report-meta-centered {{
        text-align: center;
      }}
      .report-meta p {{
        margin: 0 0 4px;
      }}
      .report-summary {{
        margin: 0 0 18px;
      }}
      .report-summary-left {{
        width: 52%;
        text-align: left;
      }}
      .report-summary-left p {{
        margin: 0 0 6px;
      }}
      .report-summary-reasons {{
        margin-top: 8px;
      }}
      .report-summary-reasons-highlight {{
        border-left: 4px solid #3b82f6;
        background: #eff6ff;
        padding: 8px 12px;
        border-radius: 8px;
      }}
      .report-summary-list {{
        margin: 0;
        padding: 0;
        list-style: none;
      }}
      .report-summary-list li {{
        padding: 2px 0;
        border-bottom: none;
      }}
      .report-summary-list li:last-child {{
        border-bottom: none;
      }}
      .report-summary-empty {{
        margin: 0;
      }}
      .right-aligned {{
        text-align: right;
      }}
      table {{
        width: 100%;
        border-collapse: collapse;
        table-layout: fixed;
      }}
      thead th {{
        background: #eef2f7;
        font-weight: 700;
      }}
      th, td {{
        border: 1px solid #9aa4b2;
        padding: 8px 10px;
        vertical-align: top;
        word-wrap: break-word;
      }}
      .col-number {{
        width: 42px;
        text-align: center;
      }}
      .text-center {{
        text-align: center;
      }}
      .signature-block {{
        margin-top: 34px;
      }}
      .signature-grid {{
        width: 100%;
        border-collapse: collapse;
      }}
      .signature-grid td {{
        border: none;
        padding: 6px 0;
        vertical-align: bottom;
      }}
      .signature-role {{
        width: 36%;
        padding-right: 18px;
      }}
      .signature-line {{
        width: 28%;
        border-bottom: 1px solid #6b7280 !important;
      }}
      .signature-name {{
        width: 36%;
        padding-left: 18px;
        text-align: center;
      }}
      .signature-date {{
        text-align: center;
        white-space: nowrap;
        font-size: 12pt;
        padding-top: 8px !important;
      }}
      .signature-date-left {{
        text-align: left;
        white-space: nowrap;
        font-size: 12pt;
        padding-top: 8px !important;
      }}
      .signature-hint {{
        font-size: 10.5pt;
        color: #6b7280;
      }}
    </style>
  </head>
  <body>
    <div class="report">
      {body}
    </div>
  </body>
</html>"""


def build_word_document(title: str, body: str, lang: str = "ru") -> bytes:
    return build_html_document(title, body, lang).encode("utf-8")


def _register_pdf_font() -> tuple[str, str]:
    regular_name = "TimesNewRomanUnicode"
    bold_name = "TimesNewRomanUnicodeBold"
    regular_path = Path(r"C:\Windows\Fonts\times.ttf")
    bold_path = Path(r"C:\Windows\Fonts\timesbd.ttf")

    registered_fonts = pdfmetrics.getRegisteredFontNames()
    if regular_name not in registered_fonts:
        pdfmetrics.registerFont(TTFont(regular_name, str(regular_path)))
    if bold_name not in registered_fonts:
        pdfmetrics.registerFont(TTFont(bold_name, str(bold_path if bold_path.exists() else regular_path)))
    return regular_name, bold_name


def build_pdf_document(title: str, metadata_lines: list[str], columns: list[str], rows: list[list[str]], signature_block: dict | None = None) -> bytes:
    font_name, bold_font_name = _register_pdf_font()
    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=18 * mm,
        bottomMargin=16 * mm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Heading1"],
        fontName=bold_font_name,
        fontSize=16,
        leading=20,
        alignment=1,
        spaceAfter=12,
    )
    meta_style = ParagraphStyle(
        "ReportMeta",
        parent=styles["Normal"],
        fontName=font_name,
        fontSize=14,
        leading=18,
        spaceAfter=2,
    )
    top_note_style = ParagraphStyle(
        "ReportTopNote",
        parent=styles["Normal"],
        fontName=font_name,
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#64748B"),
        spaceAfter=6,
    )
    cell_style = ParagraphStyle(
        "ReportCell",
        parent=styles["Normal"],
        fontName=font_name,
        fontSize=14,
        leading=17,
    )
    header_style = ParagraphStyle(
        "ReportHeader",
        parent=styles["Normal"],
        fontName=bold_font_name,
        fontSize=14,
        leading=17,
        alignment=1,
    )

    story = []
    if metadata_lines:
        story.append(Paragraph(metadata_lines[0], top_note_style))
    story.append(Paragraph(title, title_style))
    story.extend(Paragraph(line, meta_style) for line in metadata_lines[1:])
    story.append(Spacer(1, 8))

    column_count = max(len(columns), 1)
    number_width = 14 * mm if columns and columns[0] == "№" else 0
    remaining_width = document.width - number_width
    other_columns = max(column_count - (1 if number_width else 0), 1)
    col_widths = []
    for index, _ in enumerate(columns):
        if index == 0 and number_width:
            col_widths.append(number_width)
        else:
            col_widths.append(remaining_width / other_columns)

    table_data = [[Paragraph(label, header_style) for label in columns]]
    for row in rows:
        table_data.append([Paragraph(str(value), cell_style) for value in row])

    table = Table(table_data, colWidths=col_widths, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EEF2F7")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#1F2937")),
                ("GRID", (0, 0), (-1, -1), 0.7, colors.HexColor("#9AA4B2")),
                ("BOX", (0, 0), (-1, -1), 0.9, colors.HexColor("#7C8796")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (0, 0), (0, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story.append(table)

    if signature_block:
        story.append(Spacer(1, 20))

        signature_style = ParagraphStyle(
            "SignatureText",
            parent=styles["Normal"],
            fontName=font_name,
            fontSize=14,
            leading=18,
        )
        signature_hint_style = ParagraphStyle(
            "SignatureHint",
            parent=styles["Normal"],
            fontName=font_name,
            fontSize=10.5,
            leading=13,
            textColor=colors.HexColor("#6B7280"),
            alignment=1,
        )

        signature_table = Table(
            [
                [
                    Paragraph(signature_block["role"], signature_style),
                    "",
                    Paragraph(signature_block["name"], signature_style),
                ],
                [
                    Paragraph(signature_block["role_hint"], signature_hint_style),
                    Paragraph(signature_block["signature_hint"], signature_hint_style),
                    Paragraph(signature_block["name_hint"], signature_hint_style),
                ],
                [
                    Paragraph(signature_block["date"], signature_style),
                    "",
                    "",
                ],
                [
                    Paragraph(signature_block["date_hint"], signature_hint_style),
                    "",
                    "",
                ],
            ],
            colWidths=[document.width * 0.36, document.width * 0.28, document.width * 0.36],
        )
        signature_table.setStyle(
            TableStyle(
                [
                    ("LINEBELOW", (1, 0), (1, 0), 0.9, colors.HexColor("#6B7280")),
                    ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                    ("ALIGN", (1, 0), (2, 3), "CENTER"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )
        story.append(signature_table)

    document.build(story)
    return buffer.getvalue()


def html_response(title: str, body: str, lang: str = "ru") -> HttpResponse:
    return HttpResponse(build_html_document(title, body, lang), content_type="text/html; charset=utf-8")


def attachment_response(content: bytes, filename: str, content_type: str) -> HttpResponse:
    response = HttpResponse(content, content_type=content_type)
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
