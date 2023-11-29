import pickle
from pathlib import Path
from typing import Iterable

from ..Contracts.serializerhandlers import Serializer
from ..Exceptions import BrokenFileError


class BinarySerializer(Serializer):
    def export_to_path(self, file_path: Path, data: Iterable) -> None:
        try:
            with open(file_path, mode='wb') as bin_file:
                pickle.dump(data, bin_file, 5)
        except PermissionError as error:
            raise PermissionError(error)

    def import_from_path(self, file_path: Path) -> Iterable:
        try:
            with open(file_path, mode='rb') as bin_file:
                data = pickle.load(bin_file)
        except pickle.UnpicklingError:
            raise BrokenFileError('Could not decode file: %s' % file_path)
        return data
