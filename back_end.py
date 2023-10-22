from typing import Callable, Optional
from tkinter.messagebox import showinfo, showerror, showwarning, askyesnocancel, askretrycancel

from customtkinter import (StringVar, BooleanVar, IntVar, CTkCheckBox, CTkRadioButton, END, NSEW, CTk, CTkImage,
                           CTkScrollableFrame)

from BackEndFunctions import ConfigurationManager, FileManager, QuestionsManager, SpellerManager, ImageManager
from BackEndFunctions.Constants import PLACE_HOLDER_PESO, PLACE_HOLDER_TEMPO, ME, MEN, VF, D
from BackEndFunctions.aparencia import altera_aparencia, altera_escala, altera_cor_padrao

from FrontEndFunctions import CaixaDeTexto


class API:
    def __init__(self, main_window: CTk):
        self._master = main_window

        # Initiate managers
        self._file = FileManager()
        self._cnf = ConfigurationManager(
            self._file.base_dir, self._file.read_json, self._file.save_json, self._file.create_personal_dict
        )
        self._quest: QuestionsManager = QuestionsManager()
        self._speller = SpellerManager(self._cnf.PERSONAL_DICT_FILE, self._cnf.add_palavra)
        self._img = ImageManager(self._file.base_dir)

        # Variáveis de perfil
        self.var_apagar_enunciado: BooleanVar = BooleanVar(value=self._cnf.apagar_enunciado)
        self.var_aparencia_do_sistema: StringVar = StringVar(value=self._cnf.aparencia_do_sistema)
        self.var_escala_do_sistema: StringVar = StringVar(value=self._cnf.escala_do_sistema)
        self.var_cor_padrao: StringVar = StringVar(value=self._cnf.cor_padrao)
        self.var_auto_export: BooleanVar = BooleanVar(value=self._cnf.exportar_automaticamente)

        # Variaveis de configurações
        self.label_configs: dict = self._cnf.label_titulos_configs
        self.entry_configs: dict = self._cnf.entry_configs
        self.list_configs: dict = self._cnf.list_configs
        self.button_configs: dict = self._cnf.buttons_configs
        self.text_configs: dict = self._cnf.text_configs

        self.img_edit: CTkImage = self._img.bt_edit
        self.img_delete: CTkImage = self._img.bt_delete
        self.img_config: CTkImage = self._img.bt_configs

        self.category_list: list = self._cnf.categorias
        self.type_list: list = self._cnf.tipos
        self.difficulties_list: list = self._cnf.dificuldades

        # Variáveis de controle
        self.contador_de_opcoes: IntVar = IntVar(value=0)
        self.var_rd_button_value: IntVar = IntVar(value=0)
        self.display_question_count: IntVar = IntVar(value=0)
        self.exportado: bool = True

        # External event handlers
        self.start_monitor_handler = self._speller.monitora_textbox

        # Campos da questao
        self.categoria = StringVar(value=self._cnf.unidade_padrao)
        self.sub_categoria = StringVar()
        self.tempo = StringVar(value=PLACE_HOLDER_TEMPO)
        self.tipo = StringVar(value=self._cnf.tipos[1])
        self.dificuldade = StringVar(value=self._cnf.dificuldades[0])
        self.peso = StringVar(value=PLACE_HOLDER_PESO)
        self.pergunta: Optional[CaixaDeTexto] = None
        self.lista_txt_box: list[Optional[CaixaDeTexto]] = list()
        self.lista_rd_bts: list[Optional[CTkRadioButton]] = list()
        self.lista_ck_bts: list[Optional[CTkCheckBox]] = list()

        # Quadro de questões
        self.frame_questoes: Optional[CTkScrollableFrame] = None

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

    def reseta_informacoes(self):
        # Janela de parâmetros
        self.categoria.set(self._cnf.unidade_padrao)
        self.sub_categoria.set('')
        self.tempo.set(PLACE_HOLDER_TEMPO)
        self.tipo.set(self._cnf.tipos[1])
        self.dificuldade.set(self._cnf.dificuldades[0])
        self.peso.set(PLACE_HOLDER_PESO)

        # Janela de enunciado
        if self.var_apagar_enunciado:
            self.pergunta.delete(0.0, END)

        # Janela de botões
        self.var_rd_button_value.set(0)
        for bt in self.lista_ck_bts:
            bt.deselect()
        for txt_box in self.lista_txt_box:
            txt_box.delete(0.0, END)
            self.rm_choice_handler()

        self.pergunta.focus()

    def add_choice_handler(self, texto_alternativa=None, indice=None) -> None:
        if self.contador_de_opcoes.get() == len(self.lista_txt_box) or self.tipo.get() == D:
            showinfo('Limite de opções', 'Quantidade limite de opções atingida')
            return None

        # Ativado pela alteração de tipo de questão
        if indice is None: indice = self.contador_de_opcoes.get()

        # Se a linha for zero, seta como 50, do contrário, 10
        pady = (5 if not indice else 10, 0)

        self.lista_txt_box[indice].grid(column=0, row=indice, sticky=NSEW, pady=pady)

        # Ativado pela edição de questão
        if texto_alternativa is not None: self.lista_txt_box[indice].insert(1.0, texto_alternativa)

        bt = self._get_opcao_bt(indice, self.tipo.get())
        bt.grid(column=1, row=indice, padx=(10, 0), pady=pady)

        self.contador_de_opcoes.set(self.contador_de_opcoes.get() + 1)

    def rm_choice_handler(self, indice=None) -> None:
        # Se for zero signifca que não tem opção exibida e cancela a ação
        if not self.contador_de_opcoes.get():
            return None

        self.contador_de_opcoes.set(self.contador_de_opcoes.get() - 1)

        # Ativado pela edição de questão
        if indice is None:
            indice = self.contador_de_opcoes.get()

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

    def delete_question(self, controle: int) -> None:
        if self._quest.remove_question(controle):
            showinfo('Questão deletada', 'A questão foi deletada com sucesso!')

    def editar_questao(self, controle: int) -> None:
        self.reseta_informacoes()
        question_info: dict = self._quest.get_question_data(controle)
        self.categoria.set(question_info.get('categoria'))
        self.sub_categoria.set(question_info.get('sub_categoria'))
        self.tempo.set(question_info.get('tempo'))
        self.tipo.set(question_info.get('tipo'))
        self.dificuldade.set(question_info.get('dificuldade'))
        self.peso.set(question_info.get('peso'))
        self.pergunta.insert(1.0, question_info.get('pergunta'))

    def configs_window_handler(self):
        painel = self._master.children.get('!janeladeconfiguracoes')
        if painel: return painel.wm_deiconify()

        # PainelDeConfiguracoes(self, self.gvar)

    def save_question_handler(self):
        if not self.gvar.pergunta.get_texto_completo() or self.verifica_texto_opcoes():
            return showwarning(
                'Pergunta em branco',
                'Para salvar uma questão é necessário que a pergunta e as np_alternativas ativas não esteja em '
                'branco.'
            )

        if self.gvar.questao_em_edicao:
            self.salvar_edicao()
            return

        if self.gvar.quadro_de_questoes.verifica_se_pergunta_ja_existe():
            return showinfo('Pergunta repetida', 'Já existe uma questão com a mesma pergunta')

        questao = QuestionDataClass(
            self.gvar.unidade.get(), self.gvar.sub_categoria.get(), self.gvar.tempo.get(),
            self.gvar.tipo.get(), self.gvar.dificuldade.get(), self.gvar.peso.get(),
            self.gvar.pergunta.get_texto_completo(), self.get_opcoes()
        )
        self.gvar.quadro_de_questoes.adiciona_questao(questao)

        self.gvar.reseta_informacoes()
        self.gvar.exportado = False

    def verifica_texto_opcoes(self):
        if self.gvar.tipo.get() != D:
            if not self.gvar.contador_de_opcoes.get():
                return True
            for indice in range(self.gvar.contador_de_opcoes.get()):
                opcao: CaixaDeTexto = self.gvar.lista_txt_box[indice]
                if not opcao.get_texto_completo():
                    return True
        return False

    def salvar_edicao(self):
        self._quest.create_new_question(

        )
        self.categoria = self.gvar.unidade.get()
        self.gvar.questao_em_edicao.subcategoria = self.gvar.sub_categoria.get()
        self.gvar.questao_em_edicao.tempo = self.gvar.tempo.get()
        self.gvar.questao_em_edicao.tipo = self.gvar.tipo.get()
        self.gvar.questao_em_edicao.dificuldade = self.gvar.dificuldade.get()
        self.gvar.questao_em_edicao.peso = self.gvar.peso.get()
        self.gvar.questao_em_edicao.pergunta = self.gvar.pergunta.get_texto_completo()
        self.gvar.questao_em_edicao.alternativas = self.get_opcoes()

        self.gvar.quadro_de_questoes.salvar_edicao_de_questao()

        self.gvar.questao_em_edicao = None
        self.gvar.reseta_informacoes()

    def get_opcoes(self) -> list[tuple[str, bool]]:
        def seleciona_bt(indice: int) -> [CTkRadioButton, CTkCheckBox]:
            tipo = self.gvar.tipo.get()
            if tipo == ME:
                return self.gvar.lista_rd_bts[indice]
            elif tipo == MEN or tipo == VF:
                return self.gvar.lista_ck_bts[indice]

        def verifica_correta(botao: [CTkRadioButton, CTkCheckBox], indice: int) -> bool:
            if self.gvar.tipo.get() == ME:
                return self.gvar.var_rd_button_value.get() == indice
            return botao.get()

        opcoes = list()
        for indice in range(self.gvar.contador_de_opcoes.get()):
            txt_box: CaixaDeTexto = self.gvar.lista_txt_box[indice]
            texto = txt_box.get_texto_completo()

            correta = verifica_correta(seleciona_bt(indice), indice)

            opcoes.append((texto, correta))

        return opcoes

    def export_handler(self):
        if self.gvar.caminho_atual is None:
            self.gvar.caminho_atual = self.gvar.arquivos.caminho_para_salvar('Exportar')

        self.gvar.arquivos.exportar(self.gvar.caminho_atual, self.gvar.quadro_de_questoes.lista_de_questoes())

        self.gvar.exportado = True
        showinfo('Exportado', 'O banco de dados foi criado com sucesso!')

        def _create_line_frame(self, fg_color: str) -> CTkFrame:
            window = CTkFrame(self._master, fg_color=fg_color, height=45)
            window.pack(expand=True, fill=X)
            return window

        def create_new_question_line(self, title: str, controle: int):
            color = self._select_color()
            line_window = self._create_line_frame(color)

            new_question_line = LinhaDeQuestao(
                line_window, title, controle, self.img_edit, self.img_delete,
                cmd_delete=self.delete_question_line, cmd_edit=self.gvar.editar_questao
            )

            self._row_dict[controle] = {'row': line_window, 'display': new_question_line}

            self.gvar.display_question_count.set(len(self._row_dict))

        def delete_question_line(self, controle: int):
            row = self._row_dict[controle]['row']
            row.destroy()
            del self._row_dict[controle]
            self._reorder_colors()
            self.gvar.display_question_count.set(len(self._row_dict))
            self.gvar.delete_question(controle)

        def _select_color(self) -> str:
            cor = VERDE
            if self._zebrar:
                cor = TRANSPARENTE
            self._zebrar = not self._zebrar
            return cor

        def _reorder_colors(self):
            self._zebrar = True
            for row_info in self._row_dict.values():
                row_info['row'].configure(fg_color=self._select_color())

    def open_db_handler(self):
        pass


    def evento_de_fechamento_da_tela(self):
        if not self.exportado:
            resposta = askyesnocancel(
                'Salvamento pendente',
                'Uma ou mais questões estão em edição e não foram exportadas.\n'
                'Deseja exportar as alterações antes de sair?'
            )
            if resposta is None:
                return
            elif resposta:
                self.exportar()
        exit(0)


if __name__ == '__main__':
    root = CTk()
    f = API()
    root.mainloop()
