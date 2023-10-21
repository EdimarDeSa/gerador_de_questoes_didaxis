from typing import Literal

from customtkinter import CTk, CTkFrame, CTkLabel, CTkScrollableFrame, CTkImage, BOTH, X

from Constants import VERDE, TRANSPARENTE
from BackEndFunctions.configuration_manager import ConfigurationManager
from BackEndFunctions.globalvars import VariaveisGlobais
from .linha_de_questao import LinhaDeQuestao


class JanelaDeQuestoes(CTkFrame):
    def __init__(self, master: CTk, configuration_manager: ConfigurationManager, variaveis_globais: VariaveisGlobais,
                 img_edit: CTkImage, img_delete: CTkImage, **kwargs):
        super().__init__(master, **kwargs)

        self.cnf_manager = configuration_manager
        self.gvar = variaveis_globais
        self.img_edit = img_edit
        self.img_delete = img_delete

        self._master = CTkScrollableFrame(self)
        self._master.pack(fill=BOTH, expand=True)

        self._row_dict: dict[int, dict[[Literal['row'], CTkFrame], [Literal['display'], LinhaDeQuestao]]] = dict()
        self._zebrar: bool = False
        self._linha_atual: int = 0

        self._init_header()

        # ------ Adiciona variáveis globais ------ #

        self.gvar.quadro_de_questoes = self

    def _create_line_winow(self, fg_color: str) -> CTkFrame:
        window = CTkFrame(self._master, fg_color=fg_color, height=45)
        window.pack(expand=True, fill=X)
        return window

    def _init_header(self):
        color = self._select_color()
        line_window = self._create_line_winow(color)

        CTkLabel(line_window, fg_color=color, text='Enunciado').place(relx=0.01, relwidth=0.8, relheight=1)
        CTkLabel(line_window, bg_color=color, text='Editar').place(relx=0.8, relwidth=0.09, relheight=1)
        CTkLabel(line_window, bg_color=color, text='Deletar').place(relx=0.9, relwidth=0.09, relheight=1)

    def create_new_question_line(self, title: str, controle: int):
        color = self._select_color()
        line_window = self._create_line_winow(color)

        new_question_line = LinhaDeQuestao(line_window, title, controle, self.img_edit, self.img_delete,
                                           cmd_delete=self.delete_event, cmd_edit=self.gvar.editar_questao)

        self._row_dict[controle] = {'row': line_window, 'display': new_question_line}

        self.gvar.display_question_count.set(len(self._row_dict))

    def delete_event(self, controle: int):
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

    def verifica_se_pergunta_ja_existe(self) -> bool:
        perguntas = []
        if self._row_dict:
            perguntas = [questao.pergunta for questao in self.lista_de_questoes()]
        return self.gvar.pergunta.get_texto_completo() in perguntas
