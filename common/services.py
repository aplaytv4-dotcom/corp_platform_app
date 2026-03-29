from django.http import HttpResponse


def build_html_document(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="ru">
  <head>
    <meta charset="utf-8">
    <title>{title}</title>
    <style>
      body {{ font-family: Arial, sans-serif; margin: 24px; }}
      h1, h2 {{ margin-bottom: 12px; }}
      table {{ border-collapse: collapse; width: 100%; }}
      th, td {{ border: 1px solid #999; padding: 8px; text-align: left; }}
    </style>
  </head>
  <body>
    {body}
  </body>
</html>"""


def build_rtf_document(title: str, lines: list[str]) -> bytes:
    safe_lines = [line.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}") for line in lines]
    content = "\\par ".join([title] + safe_lines)
    return ("{\\rtf1\\ansi " + content + "}").encode("utf-8")


def build_simple_pdf(title: str, lines: list[str]) -> bytes:
    text = "\\n".join([title] + lines)
    safe_text = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    stream = f"BT /F1 12 Tf 50 780 Td ({safe_text}) Tj ET"
    pdf = (
        "%PDF-1.4\n"
        "1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n"
        "2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n"
        "3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
        "/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj\n"
        "4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n"
        f"5 0 obj << /Length {len(stream)} >> stream\n{stream}\nendstream endobj\n"
    )
    xref_start = len(pdf.encode("utf-8"))
    xref = (
        "xref\n0 6\n"
        "0000000000 65535 f \n"
        "0000000010 00000 n \n"
        "0000000063 00000 n \n"
        "0000000122 00000 n \n"
        "0000000248 00000 n \n"
        "0000000318 00000 n \n"
        f"trailer << /Size 6 /Root 1 0 R >>\nstartxref\n{xref_start}\n%%EOF"
    )
    return (pdf + xref).encode("utf-8")


def html_response(title: str, body: str) -> HttpResponse:
    return HttpResponse(build_html_document(title, body), content_type="text/html; charset=utf-8")


def attachment_response(content: bytes, filename: str, content_type: str) -> HttpResponse:
    response = HttpResponse(content, content_type=content_type)
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
