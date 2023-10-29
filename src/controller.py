from pathlib import Path
import subprocess
from itertools import compress

from icecream import ic

from contracts.controller import ControllerHandlers
from contracts.viewcontract import ViewContract
from contracts.model import ModelContract
from src.Hints import QuestionDataHint, Optional, SysImgHint, GroupedQuestionDBHint
from src.Constants import LINK_FEEDBACK_FORM, TYPESCONVERTER

from Exceptions import *


class Controller(ControllerHandlers):
    # ------ Initialization and Setup ------ #
    def __init__(self, views: ViewContract, models: ModelContract):
        self.models = models
        self.views = views

        self._exported = True

    def start(self) -> None:
        user_settings = self.setup_user_settings()
        images = self.setup_images()
        self.views.setup(self, user_settings, images)

        self.open_db_handler('C:/Users/Edimar/Documents/GitHub/gerador_de_questoes_didaxis/auto-py-to-exe/novo_banco.xlsx')
        # self.views.tests()
    # ------  ------ #

    # ------ Image Configuration ------ #
    def setup_images(self) -> SysImgHint:
        image_paths = {
            'configuracoes_light_mode': 'configuracoes_light_mode.png',
            'configuracoes_dark_mode': 'configuracoes_dark_mode.png',
            'eraser_light_mode': 'eraser_light_mode.png',
            'eraser_dark_mode': 'eraser_dark_mode.png',
            'edit_light_mode': 'edit_light_mode.png',
            'edit_dark_mode': 'edit_dark_mode.png',
        }
        return self.models.read_system_images(image_paths)
    # ------  ------ #

    # ------ User Settings Configuration ------ #
    def setup_user_settings(self):
        self._user_settings_path = self.models.create_path('configs/user_settings.json')

        try:
            if self._user_settings_path.exists():
                return self.models.read_user_settings(self._user_settings_path)
            return self.models.create_user_settings(self._user_settings_path)
        except BrokenFileError:
            return self.models.create_user_settings(self._user_settings_path)

    def update_user_settings_handler(self, param: str, value: str) -> None:
        self.models.update_user_settings(param, value, self._user_settings_path)
    # ------  ------ #

    # ------ Database Export and Handling ------ #
    def new_db_handler(self) -> None:
        ic('Criando novo banco')
        self.views.flush_questions()
        # self.models.new_db()

    def open_db_handler(self, filename: str) -> None:
        if not filename: return

        file_path = Path(filename).resolve()

        grouped_questions: GroupedQuestionDBHint = self.models.read_question_xlsx(file_path)

        for group in grouped_questions.values():
            temp_data = dict(group[0])

            temp_data.pop('alternativa')
            temp_data.pop('correta')

            temp_data['tipo'] = TYPESCONVERTER.get(temp_data['tipo'])

            temp_data['peso'] = int(temp_data['peso'])

            temp_data['alternativas'] = [(item['alternativa'], item['correta'] in ['CORRETA', 'V']) for item in group]

            controle = self.models.create_new_question(temp_data)
            temp_data['controle'] = controle

            self.views.insert_new_question(temp_data)

    def export_db_handler(self) -> None:
        ic('Exportado banco')

        self._exported = True
        ...

    def export_db_as_handler(self, path: str) -> None:
        # ic('Starting export', path)
        if not path: return

        self._exported = True
    # ------  ------ #

    # ------ Question Handling ------ #
    def create_question_handler(self, data: QuestionDataHint) -> int:
        control = self.models.create_new_question(data)

        question = self.read_question_handler(control)
        return

    def read_question_handler(self, control: int) -> QuestionDataHint:
        return self.models.read_question(control)

    def update_question_handler(self, data: QuestionDataHint) -> None:
        self.models.update_question(data)

    def delete_question_handler(self, control: int) -> None:
        self.models.delete_question(control)
    # ------  ------ #

    # ------ State Checking ------ #
    def check_if_file_already_exported(self) -> bool:
        return self._exported
    # ------  ------ #

    # ------ Model-Related Functions ------ #
    def get_base_filename(self) -> Optional[str]:
        return self.models.get_base_filename()

    def get_base_dir(self) -> Path:
        return self.models.get_base_dir()
    # ------  ------ #

    # ------ Feedback Sending ------ #
    def send_feedback_handler(self):
        subprocess.call(f'start {LINK_FEEDBACK_FORM}', shell=True, stdout=False)
    # ------  ------ #

    def loop(self):
        self.views.start_main_loop()
