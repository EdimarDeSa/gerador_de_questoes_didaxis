from pathlib import Path
import subprocess

from icecream import ic

from src.contracts.ControllerContracts import ControllerHandlers
from src.contracts.ViewsContracts import View
from src.model import Model
from src.Hints import QuestionDataHint, Optional
from src.Constants import LINK_FEEDBACK_FORM

class Controller(ControllerHandlers):
    def __init__(self, views: View, models: Model):
        self.models = models
        self.views = views

        self._exported = True

    def start(self) -> None:
        self.views.setup(self, self.models.user_settings, self.models.system_images)

    def loop(self):
        self.views.start_main_loop()

    def new_db_handler(self) -> None:
        ic('Criando novo banco')
        self.views.flush_questions()
        # self.models.new_db()

    def open_db_handler(self, path: str) -> None:
        ic('Abrindo banco de dados', path)
        if not path: return
        # self.views.insert_data_in_question_form(...)

    def export_db_handler(self) -> None:
        ic('Exportado banco')

        self._exported = True
        ...

    def export_db_as_handler(self, path: str) -> None:
        # ic('Starting export', path)
        if not path: return

        self._exported = True

    temp_count = -1

    def create_question_handler(self, data: QuestionDataHint) -> int:
        # ic('create', data)
        self._temp_question = data
        self._exported = False
        self.temp_count += 1
        return self.temp_count

    def read_question_handler(self, control: int) -> QuestionDataHint:
        # ic('read', control)
        return self._temp_question

    def update_question_handler(self, data: QuestionDataHint) -> None:
        # ic('update', data)
        pass

    def delete_question_handler(self, control: int) -> None:
        ic('delete', control)

    def update_user_settings_handler(self, param: str, value: str) -> None:
        self.models.save_user_settings(param, value)

    def check_if_file_already_exported(self) -> bool:
        return self._exported

    # TODO: passar isso para Model
    def get_base_file(self) -> Optional[str]:
        return ''

    # TODO: passar isso para Model
    def get_base_dir(self) -> Path:
        return self.models.base_dir

    def send_feedback_handler(self):
        subprocess.call(f'start {LINK_FEEDBACK_FORM}', shell=True, stdout=False)

