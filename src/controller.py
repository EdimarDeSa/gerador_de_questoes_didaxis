import os
from pathlib import Path
import subprocess

from src.contracts.controller import ControllerHandlers
from src.contracts.viewcontract import ViewContract
from src.contracts.model import ModelContract
from src.Hints import QuestionDataHint, Optional, SysImgHint, GroupedQuestionDBHint
from src.Constants import LINK_FEEDBACK_FORM, TYPESCONVERTER

from Exceptions import *


class Controller(ControllerHandlers):
    # ------ Initialization and Setup ------ #
    def __init__(self):
        self._exported = True

    def start(self, views: ViewContract, models: ModelContract) -> None:
        self.models = models
        self.views = views

        user_settings = self.setup_user_settings()
        images = self.setup_images()
        icon = self.models.create_path("icons/icon_bitmap.ico")

        self.views.setup(self, user_settings, images, icon)

    # ------  ------ #

    # ------ Image Configuration ------ #
    def setup_images(self) -> SysImgHint:
        image_paths = {
            "configuracoes_light_mode": "configuracoes_light_mode.png",
            "configuracoes_dark_mode": "configuracoes_dark_mode.png",
            "eraser_light_mode": "eraser_light_mode.png",
            "eraser_dark_mode": "eraser_dark_mode.png",
            "edit_light_mode": "edit_light_mode.png",
            "edit_dark_mode": "edit_dark_mode.png",
        }
        return self.models.read_system_images(image_paths)

    # ------  ------ #

    # ------ User Settings Configuration ------ #
    def setup_user_settings(self):
        self._user_settings_path = self.models.create_path("configs/user_settings.json")

        try:
            if not self._user_settings_path.exists():
                self.models.create_user_settings(self._user_settings_path)
            return self.models.read_user_settings(self._user_settings_path)
        except BrokenFileError:
            os.remove(self._user_settings_path)
            self.setup_user_settings()

    def update_user_settings_handler(self, param: str, value: str) -> None:
        self.models.update_user_settings(param, value, self._user_settings_path)

    # ------  ------ #

    # ------ Database Export and Handling ------ #
    def new_db_handler(self) -> None:
        cancel = self.confirm_export_first()

        if cancel:
            return

        self.models.flush_questions()

    def open_db_handler(self) -> None:
        file_path = self.views.dialog_open_file()

        if not file_path:
            return

        file_path = Path(file_path).resolve()

        grouped_questions: GroupedQuestionDBHint = self.models.read_question_xlsx(
            file_path
        )

        for group in grouped_questions.values():
            temp_data = dict(group[0])

            temp_data.pop("alternativa")
            temp_data.pop("correta")

            temp_data["tipo"] = TYPESCONVERTER.get(temp_data["tipo"])

            temp_data["peso"] = int(temp_data["peso"])

            temp_data["alternativas"] = [
                (item["alternativa"], item["correta"] in ["CORRETA", "V"])
                for item in group
            ]

            controle = self.models.create_new_question(temp_data)
            temp_data["controle"] = controle

            self.views.insert_new_question(temp_data)

    def export_db_handler(self) -> None:
        if not self.models.get_base_filename():
            self.export_as_db_handler()
            return

        filename = self.models.get_current_file_path()

        self.models.create_question_xlsx(filename)

        self._exported = True

    def export_as_db_handler(self) -> None:
        filename = self.views.dialog_save_as()

        if not filename:
            return

        file_path = Path(filename).resolve()

        self.models.create_question_xlsx(file_path)

        self._exported = True

    def confirm_export_first(self) -> bool:
        if not self._exported:
            confirm = self.views.dialog_yes_no_cancel()

            if confirm is None:
                return True

            if confirm:
                self.export_db_handler()
        return False

    # ------  ------ #

    # ------ Question Handling ------ #
    def create_question_handler(self, data: QuestionDataHint) -> int:
        control = self.models.create_new_question(data)

        question = self.read_question_handler(control)

        self._exported = False

        return question["controle"]

    def read_question_handler(self, control: int) -> QuestionDataHint:
        return self.models.read_question(control)

    def update_question_handler(self, data: QuestionDataHint) -> None:
        self._exported = False

        self.models.update_question(data)

    def delete_question_handler(self, control: int) -> None:
        self.models.delete_question(control)

        self._exported = False

    # ------  ------ #

    # ------ Model-Related Functions ------ #
    def get_base_filename(self) -> Optional[str]:
        return self.models.get_base_filename()

    def get_base_dir(self) -> Path:
        return self.models.get_base_dir()

    # ------  ------ #

    # ------ Feedback Sending ------ #
    def send_feedback_handler(self):
        subprocess.call(f"start {LINK_FEEDBACK_FORM}", shell=True, stdout=False)

    # ------  ------ #

    def loop(self, test_mode: bool = False, timeout: int = 5000):
        self.views.start_main_loop(test_mode, timeout)
