from abc import ABC, abstractmethod
from typing import List, Literal, Tuple, Dict

from customtkinter import *
from icecream import ic

from Views.Hints import QuestionDataHint
from Views.questioncountframe import QuestionCountFrame
from Views.questionparametersframe import QuestionParametersFrame
from Views.questionstatementframe import QuestionStatementFrame
# from Views.questionsframe import QuestionsFrame
# from Views.questionchoicesframe import QuestionChoicesFrame
# from Views.commandbuttonsframe import CommandButtonsFrame


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
    def insert_data_in_question_form(self, data: QuestionDataHint) -> None:
        pass


MenuSettingsHint = Dict[str, ...]


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

        self._set_color_theme(self.controller.user_color_theme)
        self._set_scaling(self.controller.user_scaling)
        self._set_appearance(self.controller.user_appearance_mode)

        self._setup_variables()
        self._setup_main_ui()

    def start_main_loop(self) -> None:
        self.root.mainloop()

    def get_data_from_form_question(self) -> QuestionDataHint:
        data = dict(
            categoria=self._category.get(),
            subcategoria=self._subcategory.get(),
            tempo=self._deadline.get(),
            tipo=self._question_type.get(),
            dificuldade=self._difficulty.get(),
            peso=self._question_weight.get(),
            pergunta=self._question.get(0.0, 'end-1c'),
            alternativas=self._choices_get(),
        )
        return data

    def insert_data_in_question_form(self, data: QuestionDataHint) -> None:
        self._category.set(data['categoria']),
        self._subcategory.set(data['subcategoria']),
        self._deadline.set(data['tempo']),
        self._question_type.set(data['tipo']),
        self._difficulty.set(data['dificuldade']),
        self._question_weight.set(data['peso']),
        self._question.isnert(0.0, data['pergunta']),
        self._choices_set(data['alternativas']),

    def _setup_variables(self) -> None:
        titles_font_settings = self.controller.titles_font_settings
        default_font_settings = self.controller.default_font_settings

        self._label_settings = {**titles_font_settings}
        self._entry_settings = {'exportselection': True, 'width': 180, **default_font_settings}
        self._list_settings = {'dynamic_resizing': False, 'anchor': CENTER, **default_font_settings}

        self._question_count = IntVar()

        self._category = StringVar()
        self._category_options = self.controller.category_options
        self._category_settings: MenuSettingsHint = {'variable': self._category,
                                                     'values': self._category_options}
        self._subcategory = StringVar()
        self._deadline = StringVar()
        self._question_type = StringVar()
        self._question_type_list = self.controller.question_type_list
        self._question_type_settings: MenuSettingsHint = {'variable': self._question_type,
                                                          'values': self._question_type_list,
                                                          'command': self._type_change_handler}
        self._difficulty = StringVar()
        self._difficulty_list = self.controller.difficulty_list
        self._difficulty_settings: MenuSettingsHint = {'variable': self._difficulty,
                                                       'values': self._difficulty_list}
        self._question_weight = IntVar()
        
    def _setup_main_ui(self) -> None:
        QuestionCountFrame(
            self.root, self._label_settings, self._question_count
        ).place(relx=0.01, rely=0.02, relwidth=0.08, relheight=0.19)
        # OK

        QuestionParametersFrame(
            self.root, self._label_settings, self._entry_settings, self._list_settings,
            self._category_settings, self._subcategory, self._deadline, self._question_type_settings,
            self._difficulty_settings, self._question_weight
        ).place(relx=0.1, relwidth=0.395, rely=0.02, relheight=0.19)
        # OK

        question_statement_frame = QuestionStatementFrame(
            self.root, self.label_settings, self.entry_settings,
            self._api.button_configs, self._api.add_choice_handler,
            self._api.rm_choice_handler, self._api.start_monitor_handler
        )
        question_statement_frame.place(relx=0.01, rely=0.23, relwidth=0.485, relheight=0.19)
        self._question = question_statement_frame.question

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

    def _type_change_handler(self, selection: str) -> None:
        ic(selection)

    def _set_appearance(self, param: str) -> None:
        set_appearance_mode(param)

    def _set_scaling(self, param: str) -> None:
        nova_escala_float = int(param.replace("%", "")) / 100
        set_widget_scaling(nova_escala_float)
        set_window_scaling(nova_escala_float)

    def _set_color_theme(self, config: str) -> None:
        set_default_color_theme(config)

    def _choices_get(self) -> List[Tuple[str, bool]]:
        pass

    def _choices_set(self, param: List[Tuple[str, bool]]) -> None:
        pass
