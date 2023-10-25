from abc import ABC, abstractmethod
import subprocess

from icecream import ic

from contracts import View, ControllerHandlers
from model import Model
from Hints import QuestionDataHint
from Constants import LINK_FEEDBACK_FORM


class Controller(ControllerHandlers):
    def __init__(self, views: View, models: Model):
        self.models = models
        self.views = views

        self.category_options = self.models.category_options
        self.question_type_list = self.models.question_type_list
        self.difficulty_list = self.models.difficulty_list

    def start(self) -> None:
        self.views.setup(self, self.models.user_settings, self.models.system_images)
        self.views.insert_data_in_question_form(dict(
            categoria='',
            subcategoria='',
            tempo='00:00:00',
            tipo=self.question_type_list[1],
            dificuldade=self.difficulty_list[0],
            peso='1',
        ))

        self.views.start_main_loop()

    def new_bd_handler(self) -> None:
        ...

    def open_bd_handler(self) -> None:
        ...

    def export_bd_handler(self) -> None:
        ...

    def export_as_bd_handler(self) -> None:
        ...

    def save_new_question_handler(self, data: QuestionDataHint) -> int:
        ic(data)
        return 1

    def save_editing_question_handler(self, data: QuestionDataHint):
        ...

    def save_user_settings_handler(self, param: str, value: str) -> None:
        self.models.save_user_settings(param, value)

    def send_feedback_handler(self):
        subprocess.call(f'start {LINK_FEEDBACK_FORM}', shell=True, stdout=False)
