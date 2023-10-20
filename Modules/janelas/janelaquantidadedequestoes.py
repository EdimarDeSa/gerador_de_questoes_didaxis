from customtkinter import CTk, CTkFrame, CTkLabel, S, N

from ..models.globalvars import VariaveisGlobais


class JanelaQuantidadeDeQuestoes(CTkFrame):
    def __init__(self, master: CTk, variaveis_globais: VariaveisGlobais, **kwargs):
        super().__init__(master, **kwargs)

        self.gvar = variaveis_globais

        CTkLabel(
            self, text='Total de questões:', **self.gvar.cnf_manager.label_titulos_configs, wraplength=85
        ).pack(anchor=S, expand=True)

        CTkLabel(
            self, textvariable=self.gvar.display_quantidade_de_questoes, **self.gvar.cnf_manager.label_titulos_configs
        ).pack(anchor=N, expand=True)

