from abc import ABC, abstractmethod

from .ControllerContracts import ControllerHandlers
from src.Hints import QuestionDataHint, UserSetHint, SysImgHint, Literal


class View(ABC):
    @abstractmethod
    def setup(self, controller: ControllerHandlers, user_settings: UserSetHint, system_images: SysImgHint) -> None:
        self.controller = controller
        self.user_settings = user_settings
        self.system_images = system_images
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

    @abstractmethod
    def export_db(self) -> None:
        pass

    # Base CRUD methods

    @abstractmethod
    def create_question(self) -> None:
        pass

    @abstractmethod
    def _update_question(self, data: QuestionDataHint) -> None:
        pass

    @abstractmethod
    def _delete_question(self, control: int) -> None:
        pass

    @abstractmethod
    def alert(self, alert_type: Literal['INFO', 'WARNING', 'ERROR'], title: str, message: str) -> None:
        pass

    @abstractmethod
    def close_window_event(self):
        pass