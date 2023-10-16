from Modules.models.globalvars import *


class JanelaQuantidadeDeQuestoes(CTkFrame):
    def __init__(self, master: CTk, variaveis_globais: VariaveisGlobais, **kwargs):
        super().__init__(master, **kwargs)

        self.gvar = variaveis_globais

        CTkLabel(
            self, text='Total de questões:', **self.gvar.configs.label_titulos_configs, wraplength=85
        ).pack(anchor=S, expand=ON)

        CTkLabel(
            self, textvariable=self.gvar.display_quantidade_de_questoes, **self.gvar.configs.label_titulos_configs
        ).pack(anchor=N, expand=ON)

