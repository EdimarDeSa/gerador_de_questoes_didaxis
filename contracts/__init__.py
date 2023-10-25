from abc import ABC, abstractmethod

from Hints import (
    QuestionDataHint, MenuSettingsHint, ChoicesHint, Literal, Optional, List, UserSetHint, SysImgHint
)


class ControllerHandlers(ABC):
    @abstractmethod
    def export_bd_handler(self) -> None:
        ...

    @abstractmethod
    def save_new_question_handler(self, data: QuestionDataHint) -> None:
        ...

    @abstractmethod
    def save_editing_question_handler(self, data: QuestionDataHint) -> None:
        ...

    @abstractmethod
    def send_feedback_handler(self) -> None:
        ...

    @abstractmethod
    def save_user_settings_handler(self, param: str, value: str) -> None:
        ...


class View(ABC):
    @abstractmethod
    def setup(self, controller: ControllerHandlers, user_settings: UserSetHint, system_images: SysImgHint) -> None:
        ...

    @abstractmethod
    def start_main_loop(self) -> None:
        ...

    @abstractmethod
    def insert_data_in_question_form(self, data: QuestionDataHint) -> None:
        ...

    @abstractmethod
    def insert_new_question(self, data: QuestionDataHint) -> None:
        pass

    @abstractmethod
    def flush_questions(self) -> None:
        pass
