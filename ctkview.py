from abc import ABC, abstractmethod
from typing import Dict, List, Literal, Tuple

from customtkinter import *
from icecream import ic

from Views.questioncountframe import QuestionCountFrame
from Views.questionparametersframe import QuestionParametersFrame
# from Views.questionsframe import QuestionsFrame
# from Views.questionchoicesframe import QuestionChoicesFrame
# from Views.commandbuttonsframe import CommandButtonsFrame
# from Views.questionstatementframe import QuestionStatementFrame


QuestionDataHint = Dict[Literal['categoria'], str,
                        Literal['subcategoria'], str,
                        Literal['tempo'], str,
                        Literal['tipo'], str,
                        Literal['dificuldade'], str,
                        Literal['peso'], str,
                        Literal['pergunta'], str,
                        Literal['alternativas'], List[Tuple[str, bool]]]


class View(ABC):
    @abstractmethod
    def setup(self, controller) -> None:
        pass

    @abstractmethod
    def start_main_loop(self) -> None:
        pass

    @abstractmethod
    def get_data_from_form_question(self) -> QuestionDataHint:
        pass

    @abstractmethod
    def insert_environment_setting(self, settings: Dict):
        pass

    @abstractmethod
    def insert_data_in_question_form(self, data: QuestionDataHint) -> None:
        pass

class CTkView(View):
    def setup(self, controller) -> None:
        self.controller = controller

        self.root = CTk()
        largura, altura = 1500, 750
        pos_x = (self.root.winfo_screenwidth() - largura) // 2
        pos_y = (self.root.winfo_screenheight() - altura) // 2 - 35
        self.root.geometry(f'{largura}x{altura}+{pos_x}+{pos_y}')
        self.root.resizable(False, False)
        self.root.wm_iconbitmap(default='./icons/prova.ico')

        self._setup_variables()
        self._setup_main_ui()

    def _setup_variables(self) -> None:
        self._label_settings = {}
        self._entry_settings = {}
        self._list_settings = {}

        self._question_count = IntVar()

        self._category = StringVar()
        self._categories_list = []
        self._category_settings = {'variable': self._category, 'values': self._categories_list}
        self._subcategory = StringVar()
        self._deadline = StringVar()
        self._question_type = StringVar()
        self._question_type_list = []
        self._question_type_settings = {'variable': self._question_type, 'values': self._question_type_list}
        self._difficulty = StringVar()
        self._difficulty_list = []
        self._difficulty_settings = {'variable': self._difficulty, 'values': self._difficulty_list}
        self._question_weight = IntVar()
        
    def _setup_main_ui(self) -> None:
        QuestionCountFrame(
            self.root, self._label_settings, self._question_count
        ).place(relx=0.01, rely=0.02, relwidth=0.08, relheight=0.19)

        QuestionParametersFrame(
            self.root, self._entry_settings, self._label_settings, self._list_settings,
            self._category_settings, self._subcategory,
            self._deadline, self._question_type_settings,
            self._difficulty_settings, self._question_weight,
            self.type_change_handler
        ).place(relx=0.1, relwidth=0.395, rely=0.02, relheight=0.19)

        # question_statement_frame = QuestionStatementFrame(
        #     self.root, self.label_settings, self.entry_settings,
        #     self._api.button_configs, self._api.add_choice_handler,
        #     self._api.rm_choice_handler, self._api.start_monitor_handler
        # )
        # question_statement_frame.place(relx=0.01, rely=0.23, relwidth=0.485, relheight=0.19)
        # self._api.pergunta = question_statement_frame.pergunta
        #
        # QuestionChoicesFrame(
        #     self.root, self.label_settings, self._api.text_configs,
        #     self._api.var_rd_button_value, self._api.start_monitor_handler,
        #     self._api.lista_txt_box, self._api.lista_rd_bts,
        #     self._api.lista_ck_bts
        # ).place(relx=0.01, rely=0.44, relwidth=0.485, relheight=0.46)
        #
        # self._api.questions_frame = QuestionsFrame(
        #     self.root, self.label_settings, self._api.img_edit,
        #     self._api.img_delete
        # )
        # self._api.questions_frame.place(relx=0.505, rely=0.02, relwidth=0.485, relheight=0.96)
        #
        # CommandButtonsFrame(
        #     self.root, self._api.img_config, self._api.button_configs,
        #     self._api.setup_window_handler, self._api.export_handler,
        #     self._api.save_question_handler,
        # ).place(relx=0.01, rely=0.92, relwidth=0.485, relheight=0.06)
        #
        # self._api.setuptoplevel = SetupTopLevel(self.root, self._api)

    def start_main_loop(self) -> None:
        self.root.mainloop()
