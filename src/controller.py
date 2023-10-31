import os
import subprocess
from pathlib import Path

from src.Constants import LINK_FEEDBACK_FORM, TYPESCONVERTER
from src.contracts.controller import ControllerHandlers
from src.contracts.model import ModelContract
from src.contracts.viewcontract import ViewContract
from src.DataModels.imagemodel import ImageModel
from src.DataModels.usermodel import UserModel
from src.Exceptions import BrokenFileError, QuestionValidationError
from src.Hints import GroupedQuestionDBHint, Optional, QuestionDataHint


class Controller(ControllerHandlers):
    # ------ Initialization and Setup ------ #
    def __init__(self):
        self._exported = True
        self._user_settings_path: Path | None = None

    def start(self, views: ViewContract, models: ModelContract) -> None:
        self._models = models
        self._views = views

        user_settings = self._setup_user_settings()
        images = self._setup_images()
        icon = self._models.create_path('icons/icon_bitmap.ico')

        self._views.setup(self, user_settings, images, icon)

    def _setup_images(self) -> ImageModel:
        image_paths = {
            'configuracoes_light_mode': 'icons/configuracoes_light_mode.png',
            'configuracoes_dark_mode': 'icons/configuracoes_dark_mode.png',
            'eraser_light_mode': 'icons/eraser_light_mode.png',
            'eraser_dark_mode': 'icons/eraser_dark_mode.png',
            'edit_light_mode': 'icons/edit_light_mode.png',
            'edit_dark_mode': 'icons/edit_dark_mode.png',
        }
        image_paths = {
            key: self._models.create_path(value)
            for key, value in image_paths.items()
        }
        return self._models.read_system_images(image_paths)

    def _setup_user_settings(self) -> UserModel:
        self._user_settings_path = self._models.create_path(
            'configs/user_settings.json'
        )

        try:
            if not self._user_settings_path.exists():
                self._models.create_user_settings(self._user_settings_path)
            return self._models.read_user_settings(self._user_settings_path)
        except BrokenFileError:
            os.remove(self._user_settings_path)
            self._setup_user_settings()

    def update_user_settings_handler(self, **new_config) -> None:
        self._models.update_user_settings(
            self._user_settings_path, **new_config
        )

    # ------  ------ #

    # ------ Database Export and Handling ------ #
    def new_db_handler(self) -> None:
        cancel = self.export_first()

        if cancel:
            return

        self._models.flush_questions()

    def open_db_handler(self) -> None:
        file_path = self._views.dialog_open_file()

        if not file_path:
            return

        file_path = Path(file_path).resolve()

        grouped_questions: GroupedQuestionDBHint = (
            self._models.read_question_xlsx(file_path)
        )

        for group in grouped_questions.values():
            temp_data = dict(group[0])

            temp_data.pop('alternativa')
            temp_data.pop('correta')

            temp_data['tipo'] = TYPESCONVERTER.get(temp_data['tipo'])

            temp_data['peso'] = int(temp_data['peso'])

            temp_data['alternativas'] = [
                (item['alternativa'], item['correta'] in ['CORRETA', 'V'])
                for item in group
            ]

            controle = self._models.create_new_question(temp_data)
            temp_data['controle'] = controle

            self._views.insert_new_question(temp_data)

    def export_db_handler(self) -> None:
        if not self._models.get_base_filename():
            self.export_as_db_handler()
            return

        filename = self._models.get_current_file_path()

        self._models.create_question_xlsx(filename)

        self._exported = True

    def export_as_db_handler(self) -> None:
        filename = self._views.dialog_save_as()

        if not filename:
            return

        file_path = Path(filename).resolve()

        self._models.create_question_xlsx(file_path)

        self._exported = True

    def export_first(self) -> bool:
        if not self._exported:
            confirm = self._views.dialog_yes_no_cancel()

            if confirm is None:
                return False

            if confirm:
                self.export_db_handler()
        return True

    # ------  ------ #

    # ------ Question Handling ------ #
    def create_question_handler(self, data: QuestionDataHint) -> int:
        try:
            control = self._models.create_new_question(data)

            question = self.read_question_handler(control)

            self._exported = False

            return question['controle']
        except QuestionValidationError as e:
            self._views.alert(
                'ERROR', 'Criação de pergunta não autorizada', str(e)
            )
        except ConnectionError as e:
            self._views.alert(
                'ERROR', 'Falha de conexão com banco de dados', str(e)
            )

    def read_question_handler(self, control: int) -> QuestionDataHint:
        return self._models.read_question(control)

    def update_question_handler(self, data: QuestionDataHint) -> None:
        self._exported = False

        self._models.update_question(data)

    def delete_question_handler(self, control: int) -> None:
        self._models.delete_question(control)

        self._exported = False

    # ------  ------ #

    # ------ Model-Related Functions ------ #
    def get_base_filename(self) -> Optional[str]:
        return self._models.get_base_filename()

    def get_base_dir(self) -> Path:
        return self._models.get_base_dir()

    # ------  ------ #

    # ------ Feedback Sending ------ #
    def send_feedback_handler(self):
        subprocess.call(
            f'start {LINK_FEEDBACK_FORM}', shell=True, stdout=False
        )

    # ------  ------ #

    def loop(self, test_mode: bool = False, timeout: int = 5000):
        self._views.start_main_loop(test_mode, timeout)
