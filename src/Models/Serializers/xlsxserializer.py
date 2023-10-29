from pathlib import Path

from openpyxl import load_workbook, Workbook
from openpyxl.worksheet.worksheet import Worksheet

from src.contracts.serializer import Serializer
from src.Hints.hints import Iterable


class XLSXSerializer(Serializer):
    def export_to_path(self, file_path: Path, data: Iterable) -> None:
        pass

    def import_from_path(self, file_path: Path) -> Iterable:
        wb: Workbook = load_workbook(file_path, read_only=True, data_only=True)
        ws: Worksheet = wb.active
        return ws.values
