import sys
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import askyesnocancel, showerror, showinfo, showwarning

from customtkinter import (
    CENTER,
    END,
    NSEW,
    WORD,
    BooleanVar,
    CTk,
    CTkCheckBox,
    CTkFont,
    CTkFrame,
    CTkImage,
    CTkRadioButton,
    IntVar,
    StringVar,
    X,
    set_appearance_mode,
    set_default_color_theme,
    set_widget_scaling,
    set_window_scaling,
)

from src.Constants import (
    EXTENSION,
    FILETYPES,
    GREEN,
    ME,
    MEN,
    PLACE_HOLDER_PESO,
    PLACE_HOLDER_TEMPO,
    TRANSPARENT,
    VF,
    D,
)
from src.contracts.viewcontract import ViewContract
from src.DataModels.topleveltoolsmodel import TopLevelToolsModel
from src.DataModels.widgetssettingsmodel import WidgetsSettingsModel
from src.Hints import (
    ChoicesHint,
    List,
    Literal,
    MenuSettingsHint,
    Optional,
    QuestionDataHint,
    RowDict,
)
from src.Views import (
    CommandButtonsFrame,
    QuestionChoicesFrame,
    QuestionCountFrame,
    QuestionParametersFrame,
    QuestionsFrame,
    QuestionStatementFrame,
    SetupTopLevel,
)
from src.Views.binds import Binds
from src.Views.linha_de_questao import LinhaDeQuestao


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

    def start_main_loop(
        self, test_mode: bool = False, timeout: int = 200
    ) -> None:
        if test_mode:
            self._tests(timeout)

        self.root.mainloop()

    def _setup_root(self) -> None:
        self.root = CTk()

        root_width, root_height = 1500, 750
        pos_x = (self.root.winfo_screenwidth() - root_width) // 2
        pos_y = (self.root.winfo_screenheight() - root_height) // 2 - 35
        self.root.geometry(f'{root_width}x{root_height}+{pos_x}+{pos_y}')

        self.root.resizable(False, False)

        self.root.wm_iconbitmap(default=self.icon)

        self.root.title('Editor de questões')

        self.set_appearance(self.user_settings.user_appearance_mode)
        self.set_color_theme(self.user_settings.user_color_theme)
        self.set_scaling(self.user_settings.user_scaling)

    def _setup_variables(self) -> None:
        titles_font_settings = CTkFont(
            family=self.user_settings.font_family,
            size=self.user_settings.title_font_size,
            weight='bold',
        )

        default_font_settings = CTkFont(
            family=self.user_settings.font_family,
            size=self.user_settings.default_font_size,
        )

        self.widgets_settings = WidgetsSettingsModel(
            label_settings={'font': titles_font_settings},
            entry_settings={
                'exportselection': True,
                'width': 180,
                'font': default_font_settings,
            },
            list_settings={
                'dynamic_resizing': False,
                'anchor': CENTER,
                'font': default_font_settings,
            },
            button_title_settings={'font': titles_font_settings},
            button_default_settings={'font': default_font_settings},
            text_settings={
                'undo': True,
                'wrap': WORD,
                'autoseparators': True,
                'exportselection': True,
                'maxundo': 5,
            },
            scrollable_label_settings={'label_font': titles_font_settings},
        )

        self._question_count = IntVar()

        self.category = StringVar(
            value=self.user_settings.user_default_category
        )
        self._category_settings: MenuSettingsHint = {
            'variable': self.category,
            'values': self.user_settings.category_options,
            'width': 180,
            **self.widgets_settings.list_settings,
        }

        self._subcategory = StringVar()

        self._deadline = StringVar(value=PLACE_HOLDER_TEMPO)

        self.question_type = StringVar(
            value=self.user_settings.question_type_list[1]
        )
        self._question_type_settings: MenuSettingsHint = {
            'variable': self.question_type,
            'values': self.user_settings.question_type_list,
            'command': self.type_change,
            'width': 180,
            **self.widgets_settings.list_settings,
        }

        self.difficulty = StringVar(
            value=self.user_settings.difficulty_list[0]
        )
        self._difficulty_settings: MenuSettingsHint = {
            'variable': self.difficulty,
            'values': self.user_settings.difficulty_list,
            'width': 180,
            **self.widgets_settings.list_settings,
        }

        self._question_weight = IntVar(value=1)

        self._var_rd_button_value = IntVar()
        self._txt_box_list = list()
        self._rd_bts_list = list()
        self._ck_bts_list = list()
        self._choices_count = 0

        self._updating: Optional[int] = None

        self._row_dict: RowDict = dict()
        self._zebrar = True

        self.var_erase_statement = BooleanVar(
            value=self.user_settings.erase_statement
        )

        self.var_auto_export = BooleanVar(value=self.user_settings.auto_export)

        self.top_level_tools = TopLevelToolsModel(
            self.new_db,
            self.open_db,
            self.export_db,
            self.set_appearance,
            self.set_scaling,
            self.category,
            self.var_erase_statement,
            self.var_auto_export,
        )

    def _setup_images(self) -> None:
        medium = (24, 24)
        small = (16, 16)

        setup_bt_img_light = self.system_images.configuracoes_light_mode
        setup_bt_img_dark = self.system_images.configuracoes_dark_mode
        self._img_setup = CTkImage(
            setup_bt_img_light, setup_bt_img_dark, medium
        )

        delete_light = self.system_images.eraser_light_mode
        delete_dark = self.system_images.eraser_dark_mode
        self._img_delete = CTkImage(delete_light, delete_dark, small)

        edit_light = self.system_images.edit_light_mode
        edit_dark = self.system_images.edit_dark_mode
        self._img_edit = CTkImage(edit_light, edit_dark, small)

    def _setup_ui(self) -> None:
        QuestionCountFrame(
            self.root,
            self.widgets_settings.label_settings,
            self._question_count,
        ).place(relx=0.01, rely=0.02, relwidth=0.08, relheight=0.19)

        QuestionParametersFrame(
            self.root,
            self.widgets_settings.label_settings,
            self.widgets_settings.entry_settings,
            self._category_settings,
            self._subcategory,
            self._deadline,
            self._question_type_settings,
            self._difficulty_settings,
            self._question_weight,
        ).place(relx=0.1, relwidth=0.395, rely=0.02, relheight=0.19)

        # TODO: Ainda tenho que criar um jeito de colocar o spellchecker
        question_statement_frame = QuestionStatementFrame(
            self.root,
            self.widgets_settings.label_settings,
            self.widgets_settings.entry_settings,
            self.widgets_settings.button_title_settings,
            self.add_choice,
            self.rm_choice,
        )
        question_statement_frame.place(
            relx=0.01, rely=0.23, relwidth=0.485, relheight=0.19
        )
        self._question = question_statement_frame.question

        # TODO: Ainda tenho que criar um jeito de colocar o spellchecker
        QuestionChoicesFrame(
            self.root,
            self.widgets_settings.label_settings,
            self.widgets_settings.text_settings,
            self._var_rd_button_value,
            self._txt_box_list,
            self._rd_bts_list,
            self._ck_bts_list,
        ).place(relx=0.01, rely=0.44, relwidth=0.485, relheight=0.46)

        self.questions_frame = QuestionsFrame(
            self.root,
            self.widgets_settings.label_settings,
            self._img_edit,
            self._img_delete,
        )
        self.questions_frame.place(
            relx=0.505, rely=0.02, relwidth=0.485, relheight=0.96
        )

        CommandButtonsFrame(
            self.root,
            self._img_setup,
            self.widgets_settings.button_title_settings,
            self.setup_window_handler,
            self.export_db,
            self.create_question,
        ).place(relx=0.01, rely=0.92, relwidth=0.485, relheight=0.06)

        self.setuptoplevel = SetupTopLevel(
            self.root,
            self.widgets_settings,
            self.top_level_tools,
            self.controller,
            self.user_settings,
            self.system_images,
            self.icon,
        )

    def set_appearance(self, system_color_name: str) -> None:
        """
        >>> self.set_appearance('system')
        Notes:
            Seta a aparencia do app e salva essa nova aparência no arquivo do usuário.
        Args:
            system_color_name: Nome da nova aparencia, pode ser ['light', 'dark', 'system']
        """
        set_appearance_mode(system_color_name)
        self.controller.update_user_settings_handler(
            user_appearance_mode=system_color_name
        )

    def set_color_theme(self, param: str) -> None:
        set_default_color_theme(param)
        self.controller.update_user_settings_handler(user_color_theme=param)

    def set_scaling(self, param: str) -> None:
        nova_escala_float = int(param.replace('%', '')) / 100
        set_widget_scaling(nova_escala_float)
        set_window_scaling(nova_escala_float)
        self.controller.update_user_settings_handler(user_scaling=param)

    # ------  ------ #

    # ------ Question Form Data ------ #
    def _get_data_from_form_question(self) -> QuestionDataHint:
        data = {
            'id': None,
            'categoria': self.category.get(),
            'subcategoria': self._subcategory.get(),
            'controle': None,
            'tempo': self._deadline.get(),
            'tipo': self.question_type.get(),
            'dificuldade': self.difficulty.get(),
            # TODO: Validar o peso para que aceite apenas numeros
            'peso': self._question_weight.get(),
            'pergunta': self._question.get(0.0, 'end-1c'),
            'alternativas': self._choices_get(),
        }
        return data

    def _choices_get(self) -> ChoicesHint:
        choices_list: ChoicesHint = []
        _type = self.question_type.get()

        for index in range(self._choices_count):
            bt = self._select_choice_bt(index)
            correct: bool

            if _type == D:
                break

            if _type == ME:
                correct = index == self._var_rd_button_value.get()

            else:
                correct = bool(bt.get())

            txt = self._txt_box_list[index].get(0.0, 'end-1c')
            choices_list.append((txt, correct))

        return choices_list

    def insert_data_in_question_form(self, data: QuestionDataHint) -> None:
        self.category.set(data.get('categoria', ''))
        self._subcategory.set(data.get('subcategoria', ''))
        self._deadline.set(data.get('tempo', '00:00:00'))
        self.question_type.set(data.get('tipo', ''))
        self.difficulty.set(data.get('dificuldade', 'Fácil'))
        self._question_weight.set(data.get('peso', 1))
        self._question.insert(0.0, data.get('pergunta', ''))
        self._choices_set(data.get('alternativas', [('', False)]))

        self._question.focus()

    def type_change(self, _=None) -> None:
        quantidade_de_opcoes = self._choices_count
        for indice in range(quantidade_de_opcoes):
            self.rm_choice(indice=indice)
            self.add_choice(index=indice)

    def _choices_set(self, choices_data: ChoicesHint) -> None:
        if choices_data is None:
            return

        for txt, correct in choices_data:
            self.add_choice(texto_alternativa=txt, corret=correct)

    def add_choice(
        self,
        *,
        texto_alternativa: str = None,
        index: int = None,
        corret: bool = None,
    ) -> None:
        if self.question_type.get() == D:
            return

        if self._choices_count == len(self._txt_box_list):
            self.alert(
                'INFO',
                'Limite de opções atingido',
                'Quantidade limite de opções atualmente é 10',
            )
            return

        # Ativado pela alteração de tipo de questão
        if index is None:
            index = self._choices_count

        # Se a linha for zero, seta como 5, do contrário, 10
        pady = (5 if not index else 10, 0)

        self._txt_box_list[index].grid(
            column=0, row=index, sticky=NSEW, pady=pady
        )

        # Ativado pela edição de questão
        if texto_alternativa is not None:
            self._txt_box_list[index].insert(0.0, texto_alternativa)

        bt = self._select_choice_bt(index)
        bt.grid(column=1, row=index, padx=(10, 0), pady=pady)

        if corret:
            bt.select()

        self._choices_count += 1

    def _select_choice_bt(
        self, indice: int
    ) -> Optional[CTkCheckBox | CTkRadioButton]:
        select_list = {
            ME: self._rd_bts_list,
            MEN: self._ck_bts_list,
            VF: self._ck_bts_list,
            D: None,
        }
        bt: Optional[List] = select_list.get(self.question_type.get(), None)
        if bt is None:
            return bt
        return bt[indice]

    def rm_choice(self, indice: int = None) -> None:
        # Se for zero signifca que não tem opção exibida e cancela a ação
        if not self._choices_count:
            return

        self._choices_count -= 1

        # Ativado pela edição de questão
        if indice is None:
            indice = self._choices_count

        self._txt_box_list[indice].grid_forget()
        self._ck_bts_list[indice].grid_forget()
        self._rd_bts_list[indice].grid_forget()

    # ------  ------ #

    # ------ Question List Management ------ #
    def _create_new_question_line(self, title: str, controle: int) -> None:
        color = self._select_color()
        line_frame = self._create_line_frame(color)

        new_question_line = LinhaDeQuestao(
            line_frame,
            title,
            controle,
            self._img_edit,
            self._img_delete,
            cmd_delete=self._delete_question,
            cmd_edit=self._open_question_to_update,
        )

        self._row_dict[controle] = {
            'row': line_frame,
            'display': new_question_line.title,
        }

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
        self.question_type.set(self.user_settings.question_type_list[1])
        self.difficulty.set(self.user_settings.difficulty_list[0])
        self._question_weight.set(PLACE_HOLDER_PESO)

        # Janela de enunciado
        if self.var_erase_statement:
            self._question.delete(0.0, END)

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
        if not self.controller.export_first():
            return

        self.flush_questions()

        self.controller.new_db_handler()

    def open_db(self) -> None:
        if not self.controller.export_first():
            return

        self.flush_questions()

        self.controller.open_db_handler()

    def export_db(self) -> None:
        self.controller.export_db_handler()

        self.flush_questions()

    # ------  ------ #

    # ------ Dialogs ------ #
    def dialog_save_as(self) -> str:
        filename = asksaveasfilename(
            filetypes=FILETYPES,
            defaultextension=EXTENSION,
            confirmoverwrite=True,
            initialdir=self.controller.get_base_dir(),
            initialfile=self.controller.get_base_filename(),
        )
        return filename

    def dialog_open_file(self):
        filename = askopenfilename(
            filetypes=FILETYPES,
            defaultextension=EXTENSION,
            initialdir=self.controller.get_base_dir(),
            initialfile=self.controller.get_base_filename(),
        )
        return filename

    def dialog_yes_no_cancel(self) -> Optional[bool]:
        confirm = askyesnocancel(
            title='Confirme a exportação primeiro',
            message='Você tem questões em edição, isso irá apagar as questões atuais.\n'
            'Gostaria de exportar esse banco antes?',
        )
        return confirm

    def alert(
        self,
        alert_type: Literal['INFO', 'WARNING', 'ERROR'],
        title: str,
        message: str,
    ) -> None:
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
