from pathlib import Path
from typing import Callable
from tkinter.messagebox import showinfo

from customtkinter import StringVar, BooleanVar, IntVar, CTkCheckBox, CTkRadioButton, END, NSEW

from Modules.configuration_manager import ConfigurationManager
from Modules.models.caixa_de_texto import CaixaDeTexto
from Modules.corretor_ortografico import CorretorOrtografico
from Modules.constants import PLACE_HOLDER_TEMPO, PLACE_HOLDER_PESO, D, VF, ME, MEN
from Modules.questions_manager import QuestionsManager


class API:
    def __init__(self):
        self._cnf_manager = ConfigurationManager()
        self._quest_manager = QuestionsManager()

        # Variáveis de perfil
        self.var_apagar_enunciado: BooleanVar = BooleanVar(value=self._cnf_manager.apagar_enunciado)
        self.var_exportar_automaticamente: BooleanVar = BooleanVar(value=self._cnf_manager.apagar_enunciado)
        self.var_dark_mode: StringVar = StringVar(value=self._cnf_manager.aparencia_do_sistema)

        # Variáveis de controle
        self.caminho_atual: Path | None = None
        self.contador_de_opcoes: IntVar = IntVar(value=0)
        self.opcao_correta_radio_bt: IntVar = IntVar(value=0)
        self.display_quantidade_de_questoes: IntVar = IntVar(value=0)
        self.exportado: bool = True

        # Funcoes de Controle
        self.corretor_ortografico: CorretorOrtografico | None = None
        self.exportar = None
        self.exit = None
        self.atualiza_titulo = None

        # Campos da questao
        self.categoria = StringVar(value=self._cnf_manager.unidade_padrao)
        self.sub_categoria = StringVar()
        self.tempo = StringVar(value=PLACE_HOLDER_TEMPO)
        self.tipo = StringVar(value=self._cnf_manager.tipos[1])
        self.dificuldade = StringVar(value=self._cnf_manager.dificuldades[0])
        self.peso = StringVar(value=PLACE_HOLDER_PESO)
        self.pergunta: CaixaDeTexto | None = None
        self.lista_txt_box: list[CaixaDeTexto | None] = list()
        self.lista_rd_bts: list[CTkRadioButton | None] = list()
        self.lista_ck_bts: list[CTkCheckBox | None] = list()

        # Quadro de questões
        self.quadro_de_questoes = None

    def reseta_informacoes(self):
        # Janela de parâmetros
        self.categoria.set(self._cnf_manager.unidade_padrao)
        self.sub_categoria.set('')
        self.tempo.set(PLACE_HOLDER_TEMPO)
        self.tipo.set(self._cnf_manager.tipos[1])
        self.dificuldade.set(self._cnf_manager.dificuldades[0])
        self.peso.set(PLACE_HOLDER_PESO)

        # Janela de enunciado
        if self.var_apagar_enunciado:
            self.pergunta.delete(0.0, END)

        # Janela de botões
        self.opcao_correta_radio_bt.set(0)
        for bt in self.lista_ck_bts:
            bt.deselect()
        for txt_box in self.lista_txt_box:
            txt_box.delete(0.0, END)
            self.rm_alternativa()

        self.pergunta.focus()

    def add_alternativa(self, texto_alternativa=None, indice=None) -> None:
        if self.contador_de_opcoes.get() == len(self.lista_txt_box) or self.tipo.get() == D:
            return None

        # Ativado pela alteração de tipo de questão
        if indice is None:
            indice = self.contador_de_opcoes.get()

        # Se a linha for zero, seta como 50, do contrário, 10
        pady = (5 if not indice else 10, 0)

        self.lista_txt_box[indice].grid(column=0, row=indice, sticky=NSEW, pady=pady)

        # Ativado pela edição de questão
        if texto_alternativa is not None:
            self.lista_txt_box[indice].insert(1.0, texto_alternativa)

        bt = self._get_opcao_bt(indice, self.tipo.get())
        bt.grid(column=1, row=indice, padx=(10, 0), pady=pady)

        self.contador_de_opcoes.set(self.contador_de_opcoes.get() + 1)

    def rm_alternativa(self, indice=None) -> None:
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

    def _get_opcao_bt(self, indice: int, tipo: str) -> CTkRadioButton | CTkCheckBox | None:
        bts = {
            ME: self._get_rd_bt,
            MEN: self._get_ck_bt,
            VF: self._get_ck_bt,
        }
        bt: Callable = bts.get(tipo, None)
        if bt is None:
            return bt
        return bt(indice)

    def _get_rd_bt(self, indice: int) -> CTkRadioButton:
        return self.lista_rd_bts[indice]

    def _get_ck_bt(self, indice: int) -> CTkCheckBox:
        return self.lista_ck_bts[indice]

    def altera_tipo_alternativa(self, _=None):
        quantidade_de_opcoes = self.contador_de_opcoes.get()
        for indice in range(quantidade_de_opcoes):
            self.rm_alternativa(indice=indice)
            self.add_alternativa(indice=indice)
        # self.organiza_ordem_tabulacao()

    def delete_question(self, controle: int) -> None:
        if self._quest_manager.remove_question(controle):
            showinfo('Questão deletada', 'A questão foi deletada com sucesso!')

    def editar_questao(self, controle: int) -> None:
        self.reseta_informacoes()
        question_info: dict = self._quest_manager.get_question(controle)
        self.categoria.set(question_info.get('categoria'))
        self.sub_categoria.set(question_info.get('sub_categoria'))
        self.tempo.set(question_info.get('tempo'))
        self.tipo.set(question_info.get('tipo'))
        self.dificuldade.set(question_info.get('dificuldade'))
        self.peso.set(question_info.get('peso'))
        self.pergunta.insert(1.0, question_info.get('pergunta'))
