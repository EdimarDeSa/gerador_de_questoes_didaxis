from abc import ABC, abstractmethod
import subprocess

from icecream import ic

from contracts.ControllerContracts import ControllerHandlers
from contracts.ViewsContracts import View
from model import Model
from Hints import QuestionDataHint
from Constants import LINK_FEEDBACK_FORM


class Controller(ControllerHandlers):
    def __init__(self, views: View, models: Model):
        self.models = models
        self.views = views

    def start(self) -> None:
        self.views.setup(self, self.models.user_settings, self.models.system_images)
        self.views.start_main_loop()

    def new_db_handler(self) -> None:
        ic('Criando novo banco')
        self.views.flush_questions()
        # self.models.new_db()

    def open_db_handler(self) -> None:
        ic('Abrindo banco de dados')
        # self.views.insert_data_in_question_form(...)

    def export_db_handler(self) -> None:
        ic('Exportado banco')
        ...

    def export_db_as_handler(self) -> bool:
        ic('Starting export')
        return True

    def create_question_handler(self, data: QuestionDataHint) -> int:
        ic('create', data)
        return 1

    def read_question_handler(self, control: int) -> QuestionDataHint:
        ic('read', control)
        return dict(
            categoria='',
            subcategoria='',
            tempo='00:00:00',
            tipo=self.models.user_settings['question_type_list'][1],
            dificuldade=self.models.user_settings['difficulty_list'][0],
            peso='1',
            controle=control,
            pergunta='Para atualizar',
            alternativas=[('Op1', True), ('Op2', False), ('Op3', False), ('Op4', False)]
        )

    def update_question_handler(self, data: QuestionDataHint) -> None:
        ic('update', data)

    def delete_question_handler(self, control: int) -> None:
        ic('delete', control)

    def update_user_settings_handler(self, param: str, value: str) -> None:
        self.models.save_user_settings(param, value)


    def send_feedback_handler(self):
        subprocess.call(f'start {LINK_FEEDBACK_FORM}', shell=True, stdout=False)
