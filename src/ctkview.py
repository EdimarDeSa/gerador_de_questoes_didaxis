import sys
from tkinter.messagebox import showinfo, showerror, showwarning, askyesnocancel
from tkinter.filedialog import asksaveasfilename, askopenfilename

from customtkinter import (
    CTk, CTkFrame, CTkImage, CTkCheckBox, CTkRadioButton, WORD, CENTER, NSEW, IntVar, StringVar, CTkFont,
    set_appearance_mode, set_widget_scaling, set_window_scaling, set_default_color_theme, X, BooleanVar, END
)

from src.contracts.viewcontract import ViewContract

from src.Hints import QuestionDataHint, MenuSettingsHint, ChoicesHint, RowDict, Optional, List, Literal
from src.Views import (
    QuestionCountFrame, QuestionParametersFrame, QuestionStatementFrame, QuestionChoicesFrame, QuestionsFrame,
    CommandButtonsFrame, SetupTopLevel
)
from src.Views.linha_de_questao import LinhaDeQuestao
from src.Constants import D, ME, MEN, VF, TRANSPARENT, GREEN, PLACE_HOLDER_PESO, PLACE_HOLDER_TEMPO, FILETYPES, EXTENSION
from src.Views.binds import Binds


class CTkView(ViewContract):
    # ------ Initialization and Setup ------ #
    def setup(self, controller, user_settings, system_images, icon) -> None:
        self.controller = controller
        self.user_settings = user_settings
        self.system_images = system_images
        self.icon = icon

        self._setup_root()
        self._setup_variables()
        self._setup_images()
        self._setup_ui()

        Binds(self.root, self)

    def start_main_loop(self, test_mode: bool = False, timeout: int = 200) -> None:
        if test_mode: self._tests(timeout)

        self.root.mainloop()

    def _setup_root(self) -> None:
        self.root = CTk()

        largura, altura = 1500, 750
        pos_x = (self.root.winfo_screenwidth() - largura) // 2
        pos_y = (self.root.winfo_screenheight() - altura) // 2 - 35
        self.root.geometry(f'{largura}x{altura}+{pos_x}+{pos_y}')

        self.root.resizable(False, False)

        self.root.wm_iconbitmap(default=self.icon)

        self.root.title('Editor de questões')

        self.set_scaling(self.user_settings['user_scaling'])
        self.set_appearance(self.user_settings['user_appearance_mode'])
        self.set_color_theme(self.user_settings['user_color_theme'])

    def _setup_variables(self) -> None:
        titles_font_settings = CTkFont(
            family=self.user_settings['font_family'],
            size=self.user_settings['title_font_size'],
            weight='bold'
        )
        default_font_settings = CTkFont(
            family=self.user_settings['font_family'],
            size=self.user_settings['default_font_size'],
        )

        self.label_settings = {'font': titles_font_settings}
        self.entry_settings = {'exportselection': True, 'width': 180, 'font': default_font_settings}
        self.list_settings = {'dynamic_resizing': False, 'anchor': CENTER, 'font': default_font_settings}
        self.button_title_settings = {'font': titles_font_settings}
        self.button_default_settings = {'font': default_font_settings}
        self.text_settings = {'undo': True, 'wrap': WORD, 'autoseparators': True, 'exportselection': True, 'maxundo': 5}
        self.scrollable_label_settings = {'label_font': titles_font_settings}

        self._question_count = IntVar()

        self.category = StringVar(value=self.user_settings['user_default_category'])
        self.category_options = self.user_settings['category_options']
        self._category_settings: MenuSettingsHint = {'variable': self.category,
                                                     'values': self.category_options,
                                                     'width': 180,
                                                     **self.list_settings}
        self._subcategory = StringVar()
        self._deadline = StringVar(value=PLACE_HOLDER_TEMPO)
        self._question_type_list = self.user_settings['question_type_list']
        self.question_type = StringVar(value=self._question_type_list[1])
        self._question_type_settings: MenuSettingsHint = {'variable': self.question_type,
                                                          'values': self._question_type_list,
                                                          'command': self.type_change,
                                                          'width': 180,
                                                          **self.list_settings}
        self._difficulty_list = self.user_settings['difficulty_list']
        self.difficulty = StringVar(value=self._difficulty_list[0])
        self._difficulty_settings: MenuSettingsHint = {'variable': self.difficulty,
                                                       'values': self._difficulty_list,
                                                       'width': 180,
                                                       **self.list_settings}
        self._question_weight = IntVar(value=1)

        self._var_rd_button_value = IntVar()
        self._txt_box_list = list()
        self._rd_bts_list = list()
        self._ck_bts_list = list()
        self._choices_count = 0

        self._updating: Optional[int] = None
        self._row_dict: RowDict = dict()
        self._zebrar = True

        self.var_erase_statement = BooleanVar(value=self.user_settings['erase_statement'])
        self.var_auto_export = BooleanVar(value=self.user_settings['auto_export'])

    def _setup_images(self) -> None:
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
            self.root, self.label_settings, self.entry_settings, self._category_settings,
            self._subcategory, self._deadline, self._question_type_settings,
            self._difficulty_settings, self._question_weight
        ).place(relx=0.1, relwidth=0.395, rely=0.02, relheight=0.19)

        # TODO: Ainda tenho que criar um jeito de colocar o spellchecker
        question_statement_frame = QuestionStatementFrame(
            self.root, self.label_settings, self.entry_settings, self.button_title_settings,
            self.add_choice, self.rm_choice
        )
        question_statement_frame.place(relx=0.01, rely=0.23, relwidth=0.485, relheight=0.19)
        self._question = question_statement_frame.question

        # TODO: Ainda tenho que criar um jeito de colocar o spellchecker
        QuestionChoicesFrame(
            self.root, self.label_settings, self.text_settings, self._var_rd_button_value,
            self._txt_box_list, self._rd_bts_list, self._ck_bts_list
        ).place(relx=0.01, rely=0.44, relwidth=0.485, relheight=0.46)

        self.questions_frame = QuestionsFrame(
            self.root, self.label_settings, self._img_edit, self._img_delete
        )
        self.questions_frame.place(relx=0.505, rely=0.02, relwidth=0.485, relheight=0.96)

        CommandButtonsFrame(
            self.root, self._img_setup, self.button_title_settings,
            self.setup_window_handler, self.export_db,
            self.create_question,
        ).place(relx=0.01, rely=0.92, relwidth=0.485, relheight=0.06)

        self.setuptoplevel = SetupTopLevel(self.root, self, self.controller, self.user_settings, self.system_images,
                                           self.icon)

    def set_appearance(self, param: str) -> None:
        set_appearance_mode(param)
        self.controller.update_user_settings_handler('user_appearance_mode', param)

    def set_scaling(self, param: str) -> None:
        nova_escala_float = int(param.replace("%", "")) / 100
        set_widget_scaling(nova_escala_float)
        set_window_scaling(nova_escala_float)
        self.controller.update_user_settings_handler('user_scaling', param)

    def set_color_theme(self, param: str) -> None:
        set_default_color_theme(param)
        self.controller.update_user_settings_handler('user_color_theme', param)
    # ------  ------ #

    # ------ Question Form Data ------ #
    def _get_data_from_form_question(self) -> QuestionDataHint:
        data = dict(
            id=None,
            categoria=self.category.get(),
            subcategoria=self._subcategory.get(),
            controle=None,
            tempo=self._deadline.get(),
            tipo=self.question_type.get(),
            dificuldade=self.difficulty.get(),
            # TODO: Fazer uma validação no peso para que seja possível apenas adicionar números
            peso=self._question_weight.get(),
            pergunta=self._question.get(0.0, 'end-1c'),
            alternativas=self._choices_get(),
        )
        return data

    def insert_data_in_question_form(self, data: QuestionDataHint) -> None:
        self.category.set(data.get('categoria', ''))
        self._subcategory.set(data.get('subcategoria', ''))
        self._deadline.set(data.get('tempo', '00:00:00'))
        self.question_type.set(data.get('tipo', ''))
        self.difficulty.set(data.get('dificuldade', 'Fácil'))
        self._question_weight.set(data.get('peso', 1))
        self._question.insert(0.0, data.get('pergunta', ''))
        self._choices_set(data.get('alternativas', [('', False)]))

    def type_change(self, _) -> None:
        quantidade_de_opcoes = self._choices_count
        for indice in range(quantidade_de_opcoes):
            self.rm_choice(indice=indice)
            self.add_choice(index=indice)

    def _choices_get(self) -> ChoicesHint:
        choices_list = []
        _type = self.question_type.get()
        for index in range(self._choices_count):
            bt = self._select_choice_bt(index)

            if _type == D: break

            if _type == ME: correct = index == self._var_rd_button_value.get()
            else: correct = bool(bt.get())

            txt = self._txt_box_list[index].get(0.0, 'end-1c')
            choices_list.append((txt, correct))
        return choices_list

    def _choices_set(self, choices_data: ChoicesHint) -> None:
        if choices_data is None: return
        for (txt, correct) in choices_data:
            self.add_choice(texto_alternativa=txt, corret=correct)

    def add_choice(self, *, texto_alternativa: str = None, index: int = None, corret: bool = None) -> None:
        if self.question_type.get() == self._question_type_list[0]: return

        if self._choices_count == len(self._txt_box_list):
            self.alert('INFO', 'Limite de opções', 'Quantidade limite de opções atingida')
            return None

        # Ativado pela alteração de tipo de questão
        if index is None: index = self._choices_count

        # Se a linha for zero, seta como 5, do contrário, 10
        pady = (5 if not index else 10, 0)

        self._txt_box_list[index].grid(column=0, row=index, sticky=NSEW, pady=pady)

        # Ativado pela edição de questão
        if texto_alternativa is not None: self._txt_box_list[index].insert(0.0, texto_alternativa)

        bt = self._select_choice_bt(index)
        bt.grid(column=1, row=index, padx=(10, 0), pady=pady)

        if corret:
            bt.select()

        self._choices_count += 1

    def _select_choice_bt(self, indice: int) -> Optional[CTkCheckBox | CTkRadioButton]:
        select_list = {
            ME: self._rd_bts_list,
            MEN: self._ck_bts_list,
            VF: self._ck_bts_list,
            D: None
        }
        bt: Optional[List] = select_list.get(self.question_type.get(), None)
        if bt is None: return bt
        return bt[indice]

    def rm_choice(self, indice: int = None) -> None:
        # Se for zero signifca que não tem opção exibida e cancela a ação
        if not self._choices_count: return

        self._choices_count -= 1

        # Ativado pela edição de questão
        if indice is None: indice = self._choices_count

        self._txt_box_list[indice].grid_forget()
        self._ck_bts_list[indice].grid_forget()
        self._rd_bts_list[indice].grid_forget()
    # ------  ------ #

    # ------ Question List Management ------ #
    def _create_new_question_line(self, title: str, controle: int) -> None:
        color = self._select_color()
        line_frame = self._create_line_frame(color)

        new_question_line = LinhaDeQuestao(
            line_frame, title, controle, self._img_edit, self._img_delete,
            cmd_delete=self._delete_question, cmd_edit=self._open_question_to_update
        )

        self._row_dict[controle] = {'row': line_frame, 'display': new_question_line.title}

        self._update_question_counter()

    def _delete_question(self, control: int) -> None:
        self.controller.delete_question_handler(control)

        self._remove_question_from_questions_frame(control)

    def _open_question_to_update(self, control: int) -> None:
        question = self.controller.read_question_handler(control)
        self._reset_question_form()
        self.insert_data_in_question_form(question)
        self._updating = control

    def _reset_question_form(self) -> None:
        self._subcategory.set('')
        self._deadline.set(PLACE_HOLDER_TEMPO)
        self.question_type.set(self._question_type_list[1])
        self.difficulty.set(self._difficulty_list[0])
        self._question_weight.set(PLACE_HOLDER_PESO)

        # Janela de enunciado
        if self.var_erase_statement: self._question.delete(0.0, END)

        # Janela de botões
        self._var_rd_button_value.set(0)
        total = self._choices_count
        for index in range(total):
            self._ck_bts_list[index].deselect()
            self._txt_box_list[index].delete(0.0, END)
            self.rm_choice()

        self._question.focus()

    def _update_question_counter(self) -> None:
        self._question_count.set(len(self._row_dict))

    def _remove_question_from_questions_frame(self, control: int) -> None:
        self._row_dict[control]['row'].destroy()
        del self._row_dict[control]

        self._update_question_counter()

        self._reorder_colors()

    def create_question(self) -> None:
        data = self._get_data_from_form_question()

        if self._updating:
            data['controle'] = self._updating
            self.update_question(data)
            self._updating = None
            return

        control = self.controller.create_question_handler(data)

        self._create_new_question_line(data['pergunta'], control)

        self._reset_question_form()

    def update_question(self, data: QuestionDataHint) -> None:
        self.controller.update_question_handler(data)

        updating_line = self._row_dict[self._updating]
        updating_line['display'].set(data['pergunta'])

        self._reset_question_form()

    def _reorder_colors(self) -> None:
        self._zebrar = True
        for row_info in self._row_dict.values():
            row_info['row'].configure(fg_color=self._select_color())

    def _select_color(self) -> str:
        self._zebrar = not self._zebrar
        return GREEN if self._zebrar else TRANSPARENT

    def _create_line_frame(self, fg_color: str) -> CTkFrame:
        window = CTkFrame(self.questions_frame, fg_color=fg_color, height=45)
        window.pack(expand=True, fill=X)
        return window

    def insert_new_question(self, data: QuestionDataHint) -> None:
        self._create_new_question_line(data['pergunta'], data['controle'])

    def flush_questions(self) -> None:
        questions: dict = self._row_dict.copy()
        for control in questions.keys():
            self._remove_question_from_questions_frame(control)

        self._reset_question_form()
    # ------  ------ #

    # ------ Database Functions ------ #
    def new_db(self) -> None:
        self.controller.confirm_export_first()

        self.flush_questions()

        self.controller.new_db_handler()

    def open_db(self) -> None:
        self.controller.confirm_export_first()

        self.flush_questions()

        self.controller.open_db_handler()

    def export_db(self) -> None:
        self.controller.export_db_handler()

        self.flush_questions()
    # ------  ------ #

    # ------ Dialogs ------ #
    def dialog_save_as(self) -> str:
        filename = asksaveasfilename(
            filetypes=FILETYPES, defaultextension=EXTENSION, confirmoverwrite=True,
            initialdir=self.controller.get_base_dir(), initialfile=self.controller.get_base_filename()
        )
        return filename

    def dialog_open_file(self):
        filename = askopenfilename(
            filetypes=FILETYPES, defaultextension=EXTENSION,
            initialdir=self.controller.get_base_dir(), initialfile=self.controller.get_base_filename()
        )
        return filename

    def dialog_yes_no_cancel(self) -> Optional[bool]:
        confirm = askyesnocancel(
            title='Confirme a exportação primeiro',
            message='Você tem questões em edição, isso irá apagar as questões atuais.\n'
                    'Gostaria de exportar esse banco antes?')
        return confirm

    def alert(self, alert_type: Literal['INFO', 'WARNING', 'ERROR'], title: str, message: str) -> None:
        match alert_type:
            case 'INFO':
                showinfo(title, message)
            case 'WARNING':
                showwarning(title, message)
            case 'ERROR':
                showerror(title, message)
            case _:
                return
    # ------  ------ #

    # ------ Close Window Event ------ #
    def close_window_event(self):
        self.controller.export_db_handler()

        sys.exit(0)
    # ------  ------ #

    # ------ Testing ------ #
    def _tests(self, timeout: int):
        self.root.after(timeout, self.root.destroy)
    # ------  ------ #

    # ------ Top Level ------ #
    def setup_window_handler(self) -> None:
        self.setuptoplevel.deiconify()
    # ------  ------ #
