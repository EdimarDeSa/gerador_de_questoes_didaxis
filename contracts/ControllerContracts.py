from abc import ABC, abstractmethod

from Hints import QuestionDataHint


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
    def export_db_as_handler(self) -> bool:
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
