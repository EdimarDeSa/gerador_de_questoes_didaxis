import os
import subprocess
import sys
from pathlib import Path
from functools import lru_cache
from threading import Timer, Semaphore

from src.Constants import LINK_FEEDBACK_FORM, TYPESCONVERTER
from src.Contracts.controller import ControllerHandlers
from src.Contracts.model import ModelContract
from src.Contracts.speller import SpellerContract
from src.Contracts.viewcontract import ViewContract
from src.DataModels.imagemodel import ImageModel
from src.DataModels.usermodel import UserModel
from src.Exceptions import BrokenFileError, QuestionValidationError
from src.Hints import Optional, QuestionDataHint, WidgetInfosHint
from src.Views.spelledtextbox import SpelledTextBox
from src.Speller.pyspellchecker import PySpellChecker


class Controller(ControllerHandlers):
    # ------ Initialization and Setup ------ #
    def __init__(self):
        self._exported = True
        self._user_settings_path: Path | None = None

        self._speller_deque = dict()
        self._workers_semaphore = Semaphore(3)

    def start(self, views: ViewContract, models: ModelContract) -> None:
        self._models = models
        self._views = views

        self._user_settings = self._setup_user_settings()
        images = self._setup_images()
        icon = self._models.create_path('icons/icon_bitmap.ico')

        personal_dict = self._models.create_path('configs/dicionario_pessoal.json')
        self._spellcaster: SpellerContract = PySpellChecker(personal_dict)

        self._views.setup(self, self._user_settings, images, icon)

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
        self._user_settings = self._models.update_user_settings(
            self._user_settings_path, **new_config
        )

    # ------  ------ #

    # ------ Database Export and Handling ------ #
    def new_db_handler(self) -> None:
        cancel = self.export_first()

        if cancel:
            return

        self._models.flush_questions()
        self._views.flush_questions()

    def open_db_handler(self) -> None:
        cancel = self.export_first()

        if cancel:
            return

        file_path = self._views.dialog_open_file()

        if not file_path:
            return

        file_path = Path(file_path).resolve()

        self._models.register_file_path(file_path)

        self._models.flush_questions()

        grouped_questions = self._models.read_question_xlsx(file_path)

        del file_path

        self._views.flush_questions()

        for question_dict_group in grouped_questions.values():
            temp_data: QuestionDataHint = question_dict_group[0].copy()

            temp_data.pop('alternativa')
            temp_data.pop('correta')

            temp_data['tipo'] = TYPESCONVERTER.get(temp_data['tipo'])

            temp_data['peso'] = int(temp_data['peso'])

            temp_data['alternativas'] = [
                (item['alternativa'], item['correta'] in ['CORRETA', 'V'])
                for item in question_dict_group
            ]

            controle = self._models.create_new_question(temp_data)
            temp_data['controle'] = controle

            self._views.insert_new_question(temp_data)

    def export_db_handler(self) -> None:
        if not self._models.get_base_filename():
            self.export_as_db_handler()
            return

        filename = self._models.get_current_file_path()

        question_list = self._models.get_questions_to_export_xlsx()

        self._models.save_file(filename, question_list)

        self._exported = True

        # Se estiver ativo o auto export não reseta o banco e a tabela de questões
        if self._user_settings.auto_export:
            return

        self._models.flush_questions()
        self._views.flush_questions()

    def export_as_db_handler(self) -> None:
        filename = self._views.dialog_save_as()

        if not filename:
            return

        file_path = Path(filename).resolve()

        self._models.register_file_path(file_path)

        self.export_db_handler()

    def export_first(self) -> bool:
        if not self._exported:
            confirm = self._views.dialog_yes_no_cancel()

            if confirm is None:
                return True

            if confirm:
                self.export_db_handler()
        return False

    # ------  ------ #

    # ------ Question Handling ------ #
    def create_question_handler(self, data: QuestionDataHint) -> None:
        try:
            control = self._models.create_new_question(data)
            question = self.read_question_handler(control)

            if self._user_settings.auto_export:
                self.export_db_handler()

            self._exported = False

            self._views.insert_new_question(question)
            self._views.reset_question_form()

        except QuestionValidationError as e:
            self._views.alert(
                'ERROR', 'Registro de pergunta não autorizado!', str(e)
            )
        except ConnectionError as e:
            self._views.alert(
                'ERROR', 'Falha de conexão com banco de dados!', str(e)
            )

    def read_question_handler(self, control: int) -> QuestionDataHint:
        return self._models.read_question(control)

    def update_question_handler(self, data: QuestionDataHint) -> None:
        self._models.update_question(data)

        if self._user_settings.auto_export:
            self.export_db_handler()

        self._exported = False

    def delete_question_handler(self, control: int) -> None:
        self._models.delete_question(control)

        if self._user_settings.auto_export:
            self.export_db_handler()

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

    def input_speller_queue(self, text_box_widget: SpelledTextBox) -> None:
        widget_name = str(text_box_widget.winfo_id())

        widget_infos: WidgetInfosHint = self._speller_deque.get(widget_name, None)
        if widget_infos is None:
            widget_infos = dict(widget=text_box_widget)
            self._speller_deque[widget_name] = widget_infos

        # print(self._speller_deque)
        timer: Timer = widget_infos.get('timer', None)
        print(timer)
        if timer is not None:
            timer.cancel()
            print(timer)
        # print(self._speller_deque)

        widget_infos['timer'] = self._request_timer(widget_name)
        # print(self._speller_deque)

    def _request_timer(self, widget_name: str) -> Timer:
        timer = Timer(0.5, self._start_spelling, [widget_name])
        timer.start()
        return timer

    def _start_spelling(self, widget_name: str):
        with self._workers_semaphore:
            widget_infos: WidgetInfosHint = self._speller_deque.get(widget_name)
            widget: SpelledTextBox = widget_infos.get('widget')

            if widget_infos is None:
                return

            text = widget.get(1.0, 'end-1c')

            tokens = self._spellcaster.tokenize_words(text)

            unknow_words = self._spellcaster.check_spelling(tokens)

            for word in unknow_words:
                suggestions = self._spellcaster.suggest_corrections(word)
                widget.register_suggestions(word, suggestions)



    def __limpa_correcoes_anteriores(self) -> None:
        for nome_da_tag in self.__text_widget.tag_names():
            if nome_da_tag.startswith('corretor_ortografico_'):
                self.__text_widget.remove_correcao_pela_tag(nome_da_tag)

    def show_correction_menu(self, event, palavra) -> None:
        text_widget: SpelledTextBox = event.widget._master
        pop_up_menu = Menu(text_widget, tearoff=False, font='Arial 12')
        for correction in text_widget.get_possiveis_correcoes(palavra):
            if correction == 'Sem sugestões':
                pop_up_menu.add_command(
                    label=correction, command=self.__nada_a_fazer
                )
                break
            pop_up_menu.add_command(
                label=correction,
                command=lambda c=correction, p=palavra, w=text_widget: self.__aplica_correcao(
                    c, p, w
                ),
            )
        pop_up_menu.add_separator()
        pop_up_menu.add_command(
            label=ADD,
            command=lambda c=ADD, p=palavra, w=text_widget: self.__aplica_correcao(
                c, p, w
            ),
        )
        pop_up_menu.tk_popup(x=event.x_root, y=event.y_root)

    def __aplica_correcao(self, correction, palavra, text_widget) -> None:
        start_index = text_widget.get_posicao_inicial(palavra)
        end_index = text_widget.get_posicao_final(palavra)
        tag_name = text_widget.get_nome_da_tag(palavra)
        if correction == ADD:
            self.__aplica_adicao(
                text_widget, start_index, end_index, tag_name, palavra
            )
        else:
            self.__aplica_substituicao(
                text_widget, start_index, end_index, tag_name, correction
            )
        text_widget.palavras_com_sugestoes.pop(palavra)
        text_widget.focus_set()

    def __aplica_adicao(
            self, text_widget, start_index, end_index, tag_name, palavra
    ) -> None:
        self.cmd_add_word(palavra)
        text_widget.tag_remove(tag_name, start_index, end_index)

    @staticmethod
    def __aplica_substituicao(
            text_widget, start_index, end_index, tag_name, correction
    ) -> None:
        text_widget.tag_remove(tag_name, start_index, end_index)
        text_widget.delete(start_index, end_index)
        text_widget.insert(start_index, correction)

    @staticmethod
    def __nada_a_fazer() -> None:
        pass