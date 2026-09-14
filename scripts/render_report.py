import csv
import sys
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

def render(csv_name: str, xlsx_name: str):
    with open(csv_name, encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    book = Workbook()
    sheet = book.active
    sheet.title = "Продажи по дням"
    for row in rows:
        sheet.append(row)
    for cell in sheet[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="1F4E78")
        cell.alignment = Alignment(horizontal="center")
    for column in range(1, sheet.max_column + 1):
        width = max(len(str(sheet.cell(row, column).value or "")) for row in range(1, sheet.max_row + 1)) + 2
        sheet.column_dimensions[get_column_letter(column)].width = width
    for row in range(2, sheet.max_row + 1):
        sheet.cell(row, 4).number_format = '#,##0.00 [$₽-419]'
    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = sheet.dimensions
    target = Path(xlsx_name)
    target.parent.mkdir(exist_ok=True)
    book.save(target)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Использование: render_report.py input.csv output.xlsx")
    render(sys.argv[1], sys.argv[2])
