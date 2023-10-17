from tkinter.messagebox import askyesno

from Modules.models.globalvars import *


class LinhaDeQuestao(CTkFrame):
    def __init__(
            self, master: CTkScrollableFrame, questao: ModeloQuestao, variaveis_globais: VariaveisGlobais, **kwargs
    ):
        super().__init__(master, **kwargs)
        self.gvar = variaveis_globais

        self._master = master

        self.questao: ModeloQuestao = questao

        self._label = CTkLabel(self, text=self.questao.pergunta, width=550, anchor=W, height=30, wraplength=540)
        self._label.grid(row=0, column=0, pady=5, padx=(5, 0))

        CTkButton(
            self, text=None, width=30, height=30, command=self._botao_editar,
            image=self.gvar.imagens.bt_editar_questao_img()
        ).grid(column=1, row=0, padx=15)

        CTkButton(
            self, text=None, width=30, height=30, command=self._botao_deletar,
            image=self.gvar.imagens.bt_deletar_questao_img()
        ).grid(column=2, row=0, padx=15)

    def _botao_deletar(self):
        resposta = askyesno('Deseja deletar a questão?',
                            'Tem certeza que deseja deletar a questão? Esse processo não poderá ser desfeito.')

        if resposta:
            self.gvar.delete_event(self)
            self.destroy()

    def _botao_editar(self):
        self.gvar.editar_questao(self.questao)

    def salva_questao_editada(self, nova_questao: ModeloQuestao):
        self.questao = None
        self.questao = nova_questao
        self._label.configure(text=self.questao.pergunta)
