from abc import ABC, abstractmethod
from tkinter.messagebox import showinfo, showerror, showwarning

from customtkinter import (
    CTk, CTkImage, CTkCheckBox, CTkRadioButton, WORD, CENTER, NSEW, IntVar, StringVar, set_appearance_mode,
    set_widget_scaling, set_window_scaling, set_default_color_theme
)
from icecream import ic

from Views.Hints import (
    QuestionDataHint, MenuSettingsHint, ChoicesHints, Literal, Optional, List, UserSetHint, SysImgHint
)
from Views import (
    QuestionCountFrame, QuestionParametersFrame, QuestionStatementFrame, QuestionChoicesFrame, QuestionsFrame,
    CommandButtonsFrame, SetupTopLevel
)

D = 'Dissertativa'
ME = 'Multipla escolha 1 correta'
MEN = 'Multipla escolha n corretas'
VF = 'Verdadeiro ou falso'


class View(ABC):
    @abstractmethod
    def setup(self, controller, user_settings: UserSetHint, system_images: SysImgHint) -> None:
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


class CTkView(View):
    def setup(self, controller, user_settings, system_images) -> None:
        self.controller = controller
        self.user_settings = user_settings
        self.system_images = system_images

        self._setup_root()
        self._setup_variables()
        self._setup_images()
        self._setup_ui()

    def start_main_loop(self) -> None:
        self.root.mainloop()

    def get_data_from_form_question(self) -> QuestionDataHint:
        data = dict(
            categoria=self.category.get(),
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
        self.category.set(data.get('categoria')),
        self._subcategory.set(data.get('subcategoria')),
        self._deadline.set(data.get('tempo')),
        self._question_type.set(data.get('tipo')),
        self._difficulty.set(data.get('dificuldade')),
        self._question_weight.set(data.get('peso')),
        self._question.insert(0.0, data.get('pergunta', '')),
        self._choices_set(data.get('alternativas')),

    def _setup_root(self):
        self.root = CTk()
        largura, altura = 1500, 750
        pos_x = (self.root.winfo_screenwidth() - largura) // 2
        pos_y = (self.root.winfo_screenheight() - altura) // 2 - 35
        self.root.geometry(f'{largura}x{altura}+{pos_x}+{pos_y}')
        self.root.resizable(False, False)
        self.root.wm_iconbitmap(default='./icons/prova.ico')
        self.root.title('Editor de questões')

        self.set_scaling(self.user_settings['user_scaling'])
        self.set_appearance(self.user_settings['user_appearance_mode'])
        self.set_color_theme(self.user_settings['user_color_theme'])

    def _setup_variables(self) -> None:
        titles_font_settings = self.user_settings['titles_font_settings']
        default_font_settings = self.user_settings['default_font_settings']

        self.label_settings = {**titles_font_settings}
        self._entry_settings = {'exportselection': True, 'width': 180, **default_font_settings}
        self.list_settings = {'dynamic_resizing': False, 'anchor': CENTER, **default_font_settings}
        self.button_title_settings = {**titles_font_settings}
        self.button_default_settings = {**default_font_settings}
        self._text_settings = {'undo': True, 'wrap': WORD, 'autoseparators': True,
                               'exportselection': True, 'maxundo': 5}
        self.scrollable_label_settings = {'label_font': titles_font_settings['font']}

        self._question_count = IntVar()

        self.category = StringVar()
        self.category_options = self.controller.category_options
        self._category_settings: MenuSettingsHint = {'variable': self.category,
                                                     'values': self.category_options,
                                                     'width': 180,
                                                     **self.list_settings}
        self._subcategory = StringVar()
        self._deadline = StringVar()
        self._question_type = StringVar()
        self._question_type_list = self.controller.question_type_list
        self._question_type_settings: MenuSettingsHint = {'variable': self._question_type,
                                                          'values': self._question_type_list,
                                                          'command': self._type_change_handler,
                                                          'width': 180,
                                                          **self.list_settings}
        self._difficulty = StringVar()
        self._difficulty_list = self.controller.difficulty_list
        self._difficulty_settings: MenuSettingsHint = {'variable': self._difficulty,
                                                       'values': self._difficulty_list,
                                                       'width': 180,
                                                       **self.list_settings}
        self._question_weight = IntVar()

        self._var_rd_button_value = IntVar()
        self._txt_box_lista = list()
        self._rd_bts_list = list()
        self._ck_bts_lista = list()
        self._choices_count = 0

    def _setup_images(self):
        medium = (24, 24)
        small = (16, 16)

        setup_bt_img_light = self.system_images['configuracoes_light_mode']
        setup_bt_img_dark = self.system_images['configuracoes_dark_mode']
        self._img_setup = CTkImage(setup_bt_img_light, setup_bt_img_dark, medium)

        delete_light = self.system_images['eraser_light_mode']
        delete_dark = self.system_images['eraser_dark_mode']
        self._img_delete = CTkImage(delete_light, delete_dark, small)

        edit_light = self.system_images['edit_light_mode']
        edit_dark = self.system_images['edit_dark_mode']
        self._img_edit = CTkImage(edit_light, edit_dark, small)

    def _setup_ui(self) -> None:
        QuestionCountFrame(
            self.root, self.label_settings, self._question_count
        ).place(relx=0.01, rely=0.02, relwidth=0.08, relheight=0.19)

        QuestionParametersFrame(
            self.root, self.label_settings, self._entry_settings, self._category_settings,
            self._subcategory, self._deadline, self._question_type_settings,
            self._difficulty_settings, self._question_weight
        ).place(relx=0.1, relwidth=0.395, rely=0.02, relheight=0.19)

        # TODO: Ainda tenho que criar um jeito de colocar o spellchecker
        question_statement_frame = QuestionStatementFrame(
            self.root, self.label_settings, self._entry_settings, self.button_title_settings,
            self._add_choice_handler, self._rm_choice_handler
        )
        question_statement_frame.place(relx=0.01, rely=0.23, relwidth=0.485, relheight=0.19)
        self._question = question_statement_frame.question

        # TODO: Ainda tenho que criar um jeito de colocar o spellchecker
        QuestionChoicesFrame(
            self.root, self.label_settings, self._text_settings, self._var_rd_button_value,
            self._txt_box_lista, self._rd_bts_list, self._ck_bts_lista
        ).place(relx=0.01, rely=0.44, relwidth=0.485, relheight=0.46)

        self.questions_frame = QuestionsFrame(
            self.root, self.label_settings, self._img_edit, self._img_delete
        )
        self.questions_frame.place(relx=0.505, rely=0.02, relwidth=0.485, relheight=0.96)

        CommandButtonsFrame(
            self.root, self._img_setup, self.button_title_settings,
            self.setup_window_handler, self.controller.export_bd_handler,
            self._save_question_handler,
        ).place(relx=0.01, rely=0.92, relwidth=0.485, relheight=0.06)

        self.setuptoplevel = SetupTopLevel(self.root, self, self.controller, self.user_settings, self.system_images)

    def _type_change_handler(self, _) -> None:
        quantidade_de_opcoes = self._choices_count
        for indice in range(quantidade_de_opcoes):
            self._rm_choice_handler(indice=indice)
            self._add_choice_handler(indice=indice)

    def _choices_get(self) -> ChoicesHints:
        pass

    def _choices_set(self, param: ChoicesHints) -> None:
        pass

    def _add_choice_handler(self, texto_alternativa: str = None, indice: int = None, correta: bool = None) -> None:
        if self._question_type.get() == self._question_type_list[0]: return

        if self._choices_count == len(self._txt_box_lista):
            self._alert('INFO', 'Limite de opções', 'Quantidade limite de opções atingida')
            return None

        # Ativado pela alteração de tipo de questão
        if indice is None: indice = self._choices_count

        # Se a linha for zero, seta como 5, do contrário, 10
        pady = (5 if not indice else 10, 0)

        self._txt_box_lista[indice].grid(column=0, row=indice, sticky=NSEW, pady=pady)

        # Ativado pela edição de questão
        if texto_alternativa is not None: self._txt_box_lista[indice].insert(0.0, texto_alternativa)

        bt = self._select_choice_bt(indice)
        bt.grid(column=1, row=indice, padx=(10, 0), pady=pady)

        if correta:
            bt.select()

        self._choices_count += 1

    def _select_choice_bt(self, indice: int) -> Optional[CTkCheckBox | CTkRadioButton]:
        select_list = {
            ME: self._rd_bts_list,
            MEN: self._ck_bts_lista,
            VF: self._ck_bts_lista,
            D: None
        }
        bt: Optional[List] = select_list.get(self._question_type.get(), None)
        if bt is None: return bt
        return bt[indice]

    def _rm_choice_handler(self, indice=None) -> None:
        # Se for zero signifca que não tem opção exibida e cancela a ação
        if not self._choices_count: return

        self._choices_count -= 1

        # Ativado pela edição de questão
        if indice is None: indice = self._choices_count

        self._txt_box_lista[indice].grid_forget()
        self._ck_bts_lista[indice].grid_forget()
        self._rd_bts_list[indice].grid_forget()

    def _alert(self, alert_type: Literal['INFO', 'WARNING', 'ERROR'], title: str, message: str):
        match alert_type:
            case 'INFO':
                showinfo(title, message)
            case 'WARNING':
                showwarning(title, message)
            case 'ERROR':
                showerror(title, message)
            case _:
                return

    def setup_window_handler(self):
        self.setuptoplevel.deiconify()

    # TODO: Estamos aqui
    def _save_question_handler(self):
        ic(__file__)

    def set_appearance(self, param: str) -> None:
        set_appearance_mode(param)
        if not hasattr(self, 'controller'): return
        self.controller.save_user_settings_handler('appearance_mode', param)

    def set_scaling(self, param: str) -> None:
        nova_escala_float = int(param.replace("%", "")) / 100
        set_widget_scaling(nova_escala_float)
        set_window_scaling(nova_escala_float)
        if not hasattr(self, 'controller'): return
        self.controller.save_user_settings_handler('scaling', param)

    def set_color_theme(self, param: str) -> None:
        set_default_color_theme(param)
        if not hasattr(self, 'controller'): return
        self.controller.save_user_settings_handler('color_theme', param)
