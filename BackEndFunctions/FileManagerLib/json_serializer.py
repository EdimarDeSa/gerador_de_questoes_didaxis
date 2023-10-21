from pathlib import Path
from os import remove
import json

from ..Constants import ENCODER, JSON_READER, JSON_WRITER
from ..Errors import BrokenFileError


def save_json(path: Path, data: dict | list) -> bool:
    try:
        with open(path, mode=JSON_WRITER, encoding=ENCODER) as json_file:
            json.dump(data, json_file, indent=2, sort_keys=True)
    except PermissionError as error:
        raise PermissionError(error)
    return True


def read_json(path: Path) -> dict | list:
    try:
        with open(path, mode=JSON_READER, encoding=ENCODER) as json_file:
            dictionary = json.load(json_file)
    except json.decoder.JSONDecodeError:
        remove(path)
        raise BrokenFileError('Could not decode file: %s' % path)
    return dictionary
