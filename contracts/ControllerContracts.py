from abc import ABC, abstractmethod
from pathlib import Path

from Hints import QuestionDataHint, Optional


class ControllerHandlers(ABC):
    @abstractmethod
    def new_db_handler(self) -> None:
        ...

    @abstractmethod
    def open_db_handler(self, path: str) -> None:
        ...

    @abstractmethod
    def export_db_handler(self) -> None:
        ...

    @abstractmethod
    def export_db_as_handler(self, path: str) -> None:
        ...

    @abstractmethod
    def send_feedback_handler(self) -> None:
        ...

    @abstractmethod
    def update_user_settings_handler(self, param: str, value: str) -> None:
        ...

    # Base CRUD methods

    @abstractmethod
    def create_question_handler(self, data: QuestionDataHint) -> int:
        ...

    @abstractmethod
    def read_question_handler(self, control: int) -> QuestionDataHint:
        ...

    @abstractmethod
    def update_question_handler(self, data: QuestionDataHint) -> None:
        ...

    @abstractmethod
    def delete_question_handler(self, control: int) -> None:
        ...

    @abstractmethod
    def get_base_file(self) -> Optional[str]:
        ...
    @abstractmethod
    def check_if_file_already_exported(self) -> bool:
        ...

    @abstractmethod
    def get_base_dir(self) -> Path:
        ...

