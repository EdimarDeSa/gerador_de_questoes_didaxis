import json
import pickle
import time
from pathlib import Path
import os

from ..constants import ENCODER


__all__ = ['FileSerializer']


class FileSerializer:
    @staticmethod
    def save_json(path: Path, data: dict | list) -> bool:
        try:
            with open(path, mode='w', encoding=ENCODER) as json_file:
                json.dump(data, json_file, indent=2, sort_keys=True)
        except PermissionError:
            return False
        return True

    @staticmethod
    def open_json(path: Path) -> dict | list | None:
        try:
            with open(path, mode='r', encoding=ENCODER) as json_file:
                dictionary = json.load(json_file)
        except json.decoder.JSONDecodeError:
            os.remove(path)
            return None
        return dictionary

    @staticmethod
    def open_bin(path: Path) -> str:
        with open(path, 'rb') as bin_file:
            list_palavras = pickle.load(bin_file)
        del bin_file
        return list_palavras
