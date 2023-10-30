from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterable


class Serializer(ABC):
    @abstractmethod
    def export_to_path(self, file_path: Path, data: Iterable) -> None:
        pass

    @abstractmethod
    def import_from_path(self, file_path: Path) -> Iterable:
        pass
