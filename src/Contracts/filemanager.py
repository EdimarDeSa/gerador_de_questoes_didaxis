from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class FileManagerABC(ABC):
    @abstractmethod
    def export_to_path(self, file_path: Path, data: Any) -> None:
        pass

    @abstractmethod
    def import_from_path(self, file_path: Path) -> Any:
        pass
