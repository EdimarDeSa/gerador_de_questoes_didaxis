from Modules.models.globalvars import *
from Modules.quadro_de_questoes.linha_de_questao import LinhaDeQuestao


class QuadroDeQuestoes(CTkFrame):
    def __init__(self, master: CTk, variaveis_globais: VariaveisGlobais, **kwargs):
        super().__init__(master, **kwargs)

        self.gvar = variaveis_globais

        self._master = CTkScrollableFrame(self)
        self._master.pack(fill=BOTH, expand=ON)

        self._row_list: list[LinhaDeQuestao] = list()
        self._zebrar: bool = False
        self._linha_atual: int = 0

        self._init_header()

        # ------ Adiciona variáveis globais ------ #

        self.gvar.delete_event = self.delete_event
        self.gvar.quadro_de_questoes = self

    def _init_header(self):
        cabecalho = CTkFrame(self._master, fg_color=self._select_color(), width=680)
        cabecalho.grid(row=self._linha_atual, column=0, columnspan=3, pady=2)

        cabecalho.grid_columnconfigure(0, minsize=700, weight=20)
        cabecalho.grid_columnconfigure(1, minsize=50, weight=1)
        cabecalho.grid_columnconfigure(2, minsize=50, weight=1)

        CTkLabel(cabecalho, text='Enunciado').grid(row=self._linha_atual, column=0, pady=2, padx=(2, 0))
        CTkLabel(cabecalho, text='Editar').grid(row=self._linha_atual, column=1, padx=15)
        CTkLabel(cabecalho, text='Deletar').grid(row=self._linha_atual, column=2, padx=15)
        self._add_linha()

    def adiciona_questao(self, questao: ModeloQuestao):
        nw_question_frame = LinhaDeQuestao(self._master, questao, self.gvar)
        nw_question_frame.grid(row=self._linha_atual, column=0, columnspan=3, pady=2)

        self._row_list.append(nw_question_frame)
        self._add_linha()
        self.gvar.display_quantidade_de_questoes.set(self.quantidade_de_questoes_registradas())

    def _select_color(self) -> str:
        cor = VERDE
        if self._zebrar:
            cor = TRANSPARENTE
        self._zebrar = not self._zebrar
        return cor

    def _reorder_colors(self):
        self._zebrar = True
        for row in self._row_list:
            if row.winfo_exists():
                row.configure(fg_color=self._select_color())

    def _add_linha(self):
        self._linha_atual += 1

    def delete_event(self, row: LinhaDeQuestao):
        self._row_list.remove(row)
        del row
        self._reorder_colors()
        self.gvar.display_quantidade_de_questoes.set(self.quantidade_de_questoes_registradas())

    def lista_de_questoes(self) -> list[ModeloQuestao]:
        lista = [row.questao for row in self._row_list]
        return lista

    def salvar_edicao_de_questao(self):
        for row in self._row_list:
            if row.questao == self.gvar.questao_em_edicao:
                row.salva_questao_editada(self.gvar.questao_em_edicao)

    def verifica_se_pergunta_ja_existe(self) -> bool:
        perguntas = []
        if self._row_list:
            perguntas = [questao.pergunta for questao in self.lista_de_questoes()]
        return self.gvar.pergunta.get_texto_completo() in perguntas

    def quantidade_de_questoes_registradas(self) -> int:
        total = len(self._row_list)
        return total
