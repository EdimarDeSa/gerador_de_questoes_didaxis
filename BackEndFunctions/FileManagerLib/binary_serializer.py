from pathlib import Path
import pickle
from os import remove

from ..Constants import BINARY_WRITER, BINARY_READER, BINARY_PROTOCOL
from ..Errors import BrokenFileError


def save_bin(path: Path, data: str) -> bool:
    try:
        with open(path, mode=BINARY_WRITER) as bin_file:
            pickle.dump(data, bin_file, BINARY_PROTOCOL)
    except PermissionError as error:
        raise PermissionError(error)
    return True


def read_bin(path: Path) -> str:
    try:
        with open(path, mode=BINARY_READER) as bin_file:
            blob = pickle.load(bin_file)
    except pickle.UnpicklingError:
        remove(path)
        raise BrokenFileError('Could not decode file: %s' % path)
    return blob
