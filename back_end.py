from tkinter.messagebox import showinfo, showerror, showwarning, askyesnocancel, askretrycancel
from tkinter.filedialog import askopenfilename

import pandas.errors
from customtkinter import *
from icecream import ic

from BackEndFunctions import *
from BackEndFunctions.Hints import RowHint, Optional, Callable
from BackEndFunctions.Constants import PLACE_HOLDER_PESO, PLACE_HOLDER_TEMPO, ME, MEN, VF, D, EXTENSION, FILETYPES
from BackEndFunctions.aparencia import altera_aparencia, altera_escala, altera_cor_padrao

from FrontEndFunctions.Constants import VERDE, TRANSPARENTE
from FrontEndFunctions.linha_de_questao import LinhaDeQuestao
from FrontEndFunctions import CaixaDeTexto


class Controller:
    def __init__(self, main_window: CTk):
        self._master = main_window

        # Managers
        self._file = FileManager()
        self._cnf = ConfigurationManager(
            self._file.base_dir, self._file.read_json, self._file.save_json, self._file.create_personal_dict
        )
        self._quest = QuestionsManager()
        self._speller = SpellerManager(self._cnf.PERSONAL_DICT_FILE, self._cnf.add_palavra)
        self._img = ImageManager(self._file.base_dir)

        # Variáveis de perfil
        self.var_aparencia_do_sistema: StringVar = StringVar(value=self._cnf.aparencia_do_sistema)
        self.var_escala_do_sistema: StringVar = StringVar(value=self._cnf.escala_do_sistema)
        self.var_cor_padrao: StringVar = StringVar(value=self._cnf.cor_padrao)
        self.var_erase_statement: BooleanVar = BooleanVar(value=self._cnf.apagar_enunciado)
        self.var_auto_export: BooleanVar = BooleanVar(value=self._cnf.exportar_automaticamente)

        # Variaveis de configurações
        self.label_configs: dict = self._cnf.label_titulos_configs
        self.entry_configs: dict = self._cnf.entry_configs
        self.list_configs: dict = self._cnf.list_configs
        self.button_configs: dict = self._cnf.buttons_configs
        self.text_configs: dict = self._cnf.text_configs

        # Images
        self.img_config: CTkImage = self._img.bt_configs
        self.img_edit: CTkImage = self._img.bt_edit
        self.img_delete: CTkImage = self._img.bt_delete

        self.category_list: list = self._cnf.categorias
        self.type_list: list = self._cnf.tipos
        self.difficulties_list: list = self._cnf.dificuldades

        # Variáveis de controle
        self.contador_de_opcoes: IntVar = IntVar(value=0)
        self.var_rd_button_value: IntVar = IntVar(value=0)
        self.display_question_count: IntVar = IntVar(value=0)
        self.exportado: bool = True
        self._questao_em_edicao: Optional[dict] = None

        # Variáveis da tela de questões
        self._row_dict: RowHint = dict()
        self._zebrar: bool = True
        self._linha_atual: int = 0

        # External event handlers
        self.start_monitor_handler = self._speller.monitora_textbox
        self.save_new_config_handler = self._cnf.save_new_config
        self.change_appearance_handler = altera_aparencia
        self.change_scale_handler = altera_escala

        # Campos da questao
        self.categoria = StringVar(value=self._cnf.unidade_padrao)
        self.subcategoria = StringVar()
        self.tempo = StringVar(value=PLACE_HOLDER_TEMPO)
        self.tipo = StringVar(value=self._cnf.tipos[1])
        self.dificuldade = StringVar(value=self._cnf.dificuldades[0])
        self.peso = StringVar(value=PLACE_HOLDER_PESO)
        self.pergunta: Optional[CaixaDeTexto] = None
        self.lista_txt_box: list[Optional[CaixaDeTexto]] = list()
        self.lista_rd_bts: list[Optional[CTkRadioButton]] = list()
        self.lista_ck_bts: list[Optional[CTkCheckBox]] = list()

        # Frames que são necessários acessar
        self.questions_frame: Optional[CTkScrollableFrame] = None
        self.setuptoplevel: Optional[CTkToplevel] = None

        self.configura_aparencia()
        self.change_title_handler()

    def change_title_handler(self, texto: Optional[str] = None) -> None:
        title = 'Editor de questões'

        if texto is not None: title += f' - {texto}'

        self._master.title(title)

    def configura_aparencia(self):
        # noinspection PyTypeChecker
        altera_aparencia(self.var_aparencia_do_sistema.get())
        altera_cor_padrao(self.var_cor_padrao.get())
        altera_escala(self.var_escala_do_sistema.get())

    def reset_question_form(self):
        # Janela de parâmetros
        self.categoria.set(self._cnf.unidade_padrao)
        self.subcategoria.set('')
        self.tempo.set(PLACE_HOLDER_TEMPO)
        self.tipo.set(self._cnf.tipos[1])
        self.dificuldade.set(self._cnf.dificuldades[0])
        self.peso.set(PLACE_HOLDER_PESO)

        # Janela de enunciado
        if self.var_erase_statement:
            self.pergunta.delete(0.0, END)

        # Janela de botões
        self.var_rd_button_value.set(0)
        for bt in self.lista_ck_bts:
            bt.deselect()
        for txt_box in self.lista_txt_box:
            txt_box.delete(0.0, END)
            self.rm_choice_handler()

        self.pergunta.focus()

    def add_choice_handler(self, texto_alternativa: str = None, indice: int = None, correta: bool = None) -> None:
        if self.tipo.get() == D: return None

        if self.contador_de_opcoes.get() == len(self.lista_txt_box):
            showinfo('Limite de opções', 'Quantidade limite de opções atingida')
            return None

        # Ativado pela alteração de tipo de questão
        if indice is None: indice = self.contador_de_opcoes.get()

        # Se a linha for zero, seta como 5, do contrário, 10
        pady = (5 if not indice else 10, 0)

        self.lista_txt_box[indice].grid(column=0, row=indice, sticky=NSEW, pady=pady)

        # Ativado pela edição de questão
        if texto_alternativa is not None: self.lista_txt_box[indice].insert(1.0, texto_alternativa)

        bt = self._get_opcao_bt(indice, self.tipo.get())
        bt.grid(column=1, row=indice, padx=(10, 0), pady=pady)

        if correta:
            bt.select()

        self.contador_de_opcoes.set(self.contador_de_opcoes.get() + 1)

    def rm_choice_handler(self, indice=None) -> None:
        # Se for zero signifca que não tem opção exibida e cancela a ação
        if not self.contador_de_opcoes.get(): return None

        self.contador_de_opcoes.set(self.contador_de_opcoes.get() - 1)

        # Ativado pela edição de questão
        if indice is None: indice = self.contador_de_opcoes.get()

        self.lista_txt_box[indice].grid_forget()
        self.lista_ck_bts[indice].grid_forget()
        self.lista_rd_bts[indice].grid_forget()

    def _get_opcao_bt(self, indice: int, tipo: str) -> Optional[CTkCheckBox | CTkRadioButton]:
        bts = {
            ME: self._get_rd_bt,
            MEN: self._get_ck_bt,
            VF: self._get_ck_bt,
        }
        bt: Callable[[int], Optional[CTkCheckBox | CTkRadioButton]] = bts.get(tipo, None)
        if bt is None:
            return bt
        return bt(indice)

    def _get_rd_bt(self, indice: int) -> CTkRadioButton:
        return self.lista_rd_bts[indice]

    def _get_ck_bt(self, indice: int) -> CTkCheckBox:
        return self.lista_ck_bts[indice]

    def type_change_handler(self, _=None) -> None:
        quantidade_de_opcoes = self.contador_de_opcoes.get()
        for indice in range(quantidade_de_opcoes):
            self.rm_choice_handler(indice=indice)
            self.add_choice_handler(indice=indice)
        # self.organiza_ordem_tabulacao()

    def delete_question(self, controle: int, show_info: bool = True) -> None:
        self._quest.remove_question(controle)
        if show_info:
            showinfo('Questão deletada', 'A questão foi deletada com sucesso!')

    def open_question_to_edit(self, control: int) -> None:
        # TODO: A edição está deixando escrever None na subcategoria e limpa os campos peso e tempo
        self.reset_question_form()

        try:
            question_info: dict = self._quest.get_question_data(control)
        except KeyError as e:
            showinfo('Questão inexistente', str(e))
            self.delete_question_line(control)
            return None

        self.categoria.set(question_info.get('categoria'))
        self.subcategoria.set(question_info.get('sub_categoria'))
        self.tempo.set(question_info.get('tempo'))
        self.tipo.set(question_info.get('tipo'))
        self.dificuldade.set(question_info.get('dificuldade'))
        self.peso.set(question_info.get('peso'))
        self.pergunta.insert(0.0, question_info.get('pergunta'))

        for (alternativa, correta) in question_info.get('alternativas'):
            self.add_choice_handler(alternativa, correta=correta)

        self._questao_em_edicao = question_info

    def save_question_handler(self) -> None:
        try:
            dict_infos = self._get_question_infos()

            if self._questao_em_edicao:
                self.salvar_edicao(dict_infos)
                return None

            control = self._quest.create_new_question(**dict_infos)

            question = self._quest.get_question_data(control)

            self.create_new_question_line(question.get('pergunta'), question.get('controle'))

            self.reset_question_form()
            self.exportado = False

        except Exception as e:
            raise e

        return None

    def salvar_edicao(self, dict_infos: dict) -> None:
        self._quest.edit_question(**dict_infos)

        row = self._row_dict.get(dict_infos.get('controle')).get('display')
        row.set(dict_infos.get('pergunta'))

        self._questao_em_edicao = None
        self.reset_question_form()

    def _get_opcoes(self) -> list[tuple[str, bool]]:
        def seleciona_bt(indice: int) -> [CTkRadioButton, CTkCheckBox]:
            tipo = self.tipo.get()
            if tipo == ME:
                return self.lista_rd_bts[indice]
            elif tipo == MEN or tipo == VF:
                return self.lista_ck_bts[indice]

        def verifica_correta(botao: [CTkRadioButton, CTkCheckBox], indice: int) -> bool:
            if self.tipo.get() == ME:
                return self.var_rd_button_value.get() == indice
            return botao.get()

        opcoes = list()
        for indice in range(self.contador_de_opcoes.get()):
            txt_box: CaixaDeTexto = self.lista_txt_box[indice]
            texto = txt_box.get_texto_completo()

            correta = verifica_correta(seleciona_bt(indice), indice)

            opcoes.append((texto, correta))

        return opcoes

    def export_handler(self):
        serial_quests = self._quest.serialize()

        ic(serial_quests)

        if self.caminho_atual is None:
            self.caminho_atual = self.arquivos.caminho_para_salvar('Exportar')

        self.arquivos.exportar(self.caminho_atual, self.quadro_de_questoes.lista_de_questoes())

        self.exportado = True
        showinfo('Exportado', 'O banco de dados foi criado com sucesso!')

    def _create_line_frame(self, fg_color: str) -> CTkFrame:
        window = CTkFrame(self.questions_frame, fg_color=fg_color, height=45)
        window.pack(expand=True, fill=X)
        return window

    def create_new_question_line(self, title: str, controle: int):
        color = self._select_color()
        line_frame = self._create_line_frame(color)

        new_question_line = LinhaDeQuestao(
            line_frame, title, controle, self.img_edit, self.img_delete,
            cmd_delete=self.delete_question_line, cmd_edit=self.open_question_to_edit
        )

        self._row_dict[controle] = {'row': line_frame, 'display': new_question_line.title}

        self.display_question_count.set(len(self._row_dict))

    def delete_question_line(self, controle: int, show_info: bool = True) -> None:
        row = self._row_dict[controle]['row']
        row.destroy()
        del self._row_dict[controle]
        self._reorder_colors()
        self.display_question_count.set(len(self._row_dict))
        self.delete_question(controle, show_info)

    def _select_color(self) -> str:
        self._zebrar = not self._zebrar
        return VERDE if self._zebrar else TRANSPARENTE

    def _reorder_colors(self):
        self._zebrar = True
        for row_info in self._row_dict.values():
            row_info['row'].configure(fg_color=self._select_color())

    def open_db_handler(self) -> None:
        path = askopenfilename(defaultextension=EXTENSION, filetypes=FILETYPES, initialdir=self._file.loaded_path)

        try:
            questions = self._file.open_db(path)
        except pandas.errors.InvalidColumnName as e:
            showerror('Arquivo inválido', str(e))
            return None
        except FileNotFoundError:
            return None

        self.reset_questions_frame()
        self.reset_question_form()

        for question in questions:
            control = self._quest.create_new_question(**question)

            # Desta forma eu garanto que a questão foi escrita no banco de dados antes de criar a linha
            question = self._quest.get_question_data(control)
            self.create_new_question_line(question.get('pergunta'), question.get('controle'))

    def category_change_handler(self):
        self.save_new_config_handler('unidade_padrao', self.categoria.get())

    def master_wnidow_close_event(self):
        # TODO: Variável exportado não está implementada, o programa não verifica isso ainda
        if not self.exportado:
            resposta = askyesnocancel(
                'Salvamento pendente',
                'Uma ou mais questões estão em edição e não foram exportadas.\n'
                'Deseja exportar as alterações antes de sair?'
            )
            if resposta is None:
                return
            elif resposta:
                self.export_handler()
        exit(0)

    def reset_questions_frame(self) -> None:
        qtd_questoes_atual = len(self._row_dict) + 1
        for controle in range(1, qtd_questoes_atual):
            self.delete_question_line(controle, False)

    def setup_window_handler(self):
        self.setuptoplevel.deiconify()

    def open_help_tab(self):
        self.setuptoplevel.abre_ajuda()

    def _get_question_infos(self) -> dict:
        infos = dict(
            categoria=self.categoria.get(),
            subcategoria=self.subcategoria.get(),
            tempo=self.tempo.get(),
            tipo=self.tipo.get(),
            dificuldade=self.dificuldade.get(),
            peso=self.peso.get(),
            pergunta=self.pergunta.get_texto_completo(),
            alternativas=self._get_opcoes()
        )
        if self._questao_em_edicao is not None:
            self._questao_em_edicao.update(infos)
            return self._questao_em_edicao
        return infos
