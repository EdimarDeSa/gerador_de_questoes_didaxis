import json
import pickle
from pathlib import Path

from ..constants import ENCODER


__all__ = ['FileSerializer']


class FileSerializer:
    @staticmethod
    def save_json(path: Path, data: [dict, list]) -> bool:
        try:
            with open(path, mode='w', encoding=ENCODER) as json_file:
                json.dump(data, json_file, indent=2, sort_keys=True)
        except PermissionError as err:
            raise PermissionError(err)
        return True

    @staticmethod
    def open_json(path: Path) -> dict:
        try:
            with open(path, mode='r', encoding=ENCODER) as json_file:
                dictionary = json.load(json_file)
        except PermissionError as err:
            raise PermissionError(err)
        return dictionary

    @staticmethod
    def abre_bin(path: Path) -> str:
        with open(path, 'rb') as bin_file:
            list_palavras = pickle.load(bin_file)
        del bin_file
        return list_palavras
