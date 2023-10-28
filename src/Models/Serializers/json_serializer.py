from pathlib import Path
import json

from src.Hints import Iterable
from src.contracts.serializer import Serializer

from Exceptions import BrokenFileError


class JsonSerializer(Serializer):
    def export_to_path(self, file_path: Path, data: Iterable) -> None:
        try:
            with open(file_path, mode='w', encoding='UTF-8') as json_file:
                json.dump(data, json_file, indent=2, sort_keys=True)
        except PermissionError:
            raise PermissionError('Arquivo em uso')

    def import_from_path(self, file_path: Path) -> Iterable:
        try:
            with open(file_path, mode='r', encoding='UTF-8') as json_file:
                data = json.load(json_file)
        except json.decoder.JSONDecodeError:
            raise BrokenFileError('Could not decode file: %s' % file_path)
        return data
