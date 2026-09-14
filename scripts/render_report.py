import csv
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter


def render(csv_name: str, xlsx_name: str, sheet_name: str, title: str):
    with open(csv_name, encoding="utf-8-sig", newline="") as file:
        rows = list(csv.reader(file))

    book = Workbook()
    sheet = book.active
    sheet.title = sheet_name[:31]

    last_column = max(1, len(rows[0]) if rows else 1)
    sheet.merge_cells(
        start_row=1,
        start_column=1,
        end_row=1,
        end_column=last_column,
    )

    title_cell = sheet.cell(1, 1, title)
    title_cell.font = Font(bold=True, color="FFFFFF", size=14)
    title_cell.fill = PatternFill("solid", fgColor="17365D")
    title_cell.alignment = Alignment(horizontal="center")

    for source_row in rows:
        sheet.append(source_row)

    header_row = 2
    header_fill = PatternFill("solid", fgColor="1F4E78")
    thin = Side(style="thin", color="D9E2F3")

    for cell in sheet[header_row]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = header_fill
        cell.alignment = Alignment(
            horizontal="center",
            vertical="center",
            wrap_text=True,
        )
        cell.border = Border(bottom=thin)

    for row in range(header_row + 1, sheet.max_row + 1):
        for column in range(1, sheet.max_column + 1):
            cell = sheet.cell(row, column)
            cell.alignment = Alignment(vertical="top")

            if row % 2 == 0:
                cell.fill = PatternFill("solid", fgColor="EAF2F8")

            cell.border = Border(bottom=thin)

    for column in range(1, sheet.max_column + 1):
        values = [
            str(sheet.cell(row, column).value or "")
            for row in range(1, sheet.max_row + 1)
        ]
        width = min(max(max(map(len, values)) + 2, 12), 32)
        sheet.column_dimensions[get_column_letter(column)].width = width

    for row in range(header_row + 1, sheet.max_row + 1):
        for column in range(1, sheet.max_column + 1):
            header = str(sheet.cell(header_row, column).value or "")
            if "₽" in header:
                sheet.cell(row, column).number_format = '#,##0.00 [$₽-419]'

    sheet.freeze_panes = "A3"
    sheet.auto_filter.ref = (
        f"A{header_row}:"
        f"{get_column_letter(sheet.max_column)}{sheet.max_row}"
    )

    target = Path(xlsx_name)
    target.parent.mkdir(exist_ok=True)
    book.save(target)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise SystemExit(
            "Использование: render_report.py "
            "input.csv output.xlsx sheet_name title"
        )

    render(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
