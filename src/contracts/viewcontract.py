from abc import ABC, abstractmethod

from .controller import ControllerHandlers
from src.Hints import QuestionDataHint, UserSetHint, SysImgHint, Literal


class ViewContract(ABC):
    @abstractmethod
    def setup(self, controller: ControllerHandlers, user_settings: UserSetHint, system_images: SysImgHint) -> None:
        self.controller = controller
        self.user_settings = user_settings
        self.system_images = system_images

    @abstractmethod
    def start_main_loop(self, test_mode: bool = False, timeout: int = 5000) -> None:
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
    def new_db(self) -> None:
        pass

    @abstractmethod
    def export_db(self) -> None:
        pass

    # Base CRUD methods

    @abstractmethod
    def create_question(self) -> None:
        pass

    @abstractmethod
    def update_question(self, data: QuestionDataHint) -> None:
        pass

    @abstractmethod
    def _delete_question(self, control: int) -> None:
        pass

    @abstractmethod
    def alert(self, alert_type: Literal['INFO', 'WARNING', 'ERROR'], title: str, message: str) -> None:
        pass

    @abstractmethod
    def close_window_event(self) -> None:
        pass

    @abstractmethod
    def dialog_save_as(self) -> str:
        pass

    @abstractmethod
    def dialog_open_file(self) -> str:
        pass

    @abstractmethod
    def dialog_yes_no_cancel(self) -> bool | None:
        pass
