from src.create_source_db import ROWS

def test_source_row_preserves_sale_values():
    row = ROWS[0]
    assert row[0] == "S-1001"
    assert row[1] == "2026-09-01"
    assert row[5] == "978-5-00001-001-1"
    assert row[9] == 1
    assert row[10] == 1490.00
