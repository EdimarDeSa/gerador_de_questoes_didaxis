from abc import ABC, abstractmethod
from pathlib import Path

from src.Contracts.spelledtextbox import SpelledTextBoxContract
from src.Hints.hints import Optional, QuestionDataHint


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
    def export_first(self) -> bool:
        """Returns if user want to cancel or not"""
        ...

    @abstractmethod
    def send_feedback_handler(self) -> None:
        ...

    @abstractmethod
    def update_user_settings_handler(self, **new_config) -> None:
        ...

    # Base CRUD methods

    @abstractmethod
    def create_question_handler(self, data: QuestionDataHint) -> None:
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

    @abstractmethod
    def input_speller_queue(
        self, text_box_widget: SpelledTextBoxContract
    ) -> None:
        ...

    @abstractmethod
    def add_word_in_personal_dict_handler(self, word: str) -> None:
        ...
