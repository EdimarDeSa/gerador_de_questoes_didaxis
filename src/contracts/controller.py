from abc import ABC, abstractmethod
from pathlib import Path

from src.Hints.hints import QuestionDataHint, Optional


class ControllerHandlers(ABC):
    @abstractmethod
    def new_db_handler(self) -> None:
        ...

    @abstractmethod
    def open_db_handler(self) -> None:
        ...

    @abstractmethod
    def export_db_handler(self) -> None:
        ...

    @abstractmethod
    def confirm_export_first(self) -> bool:
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
    def get_base_filename(self) -> Optional[str]:
        ...

    @abstractmethod
    def get_base_dir(self) -> Path:
        ...