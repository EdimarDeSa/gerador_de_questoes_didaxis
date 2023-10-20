from customtkinter import CTkFrame, CTk, CTkLabel, CTkOptionMenu, CTkEntry, CENTER

from ..configuration_manager import ConfigurationManager
from ..models.globalvars import VariaveisGlobais


class JanelaParametrosDaQuestao(CTkFrame):
    def __init__(self, master: CTk, cnf_manager: ConfigurationManager, variaveis_globais: VariaveisGlobais, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0, 1, 2), weight=1)

        self.cnf_manager = cnf_manager
        self.gvar = variaveis_globais

        list_configs = self.cnf_manager.list_configs
        label_configs = self.cnf_manager.label_titulos_configs
        entry_configs = self.cnf_manager.entry_configs

        CTkLabel(self, **label_configs, text='Unidade').grid(column=0, row=0)
        CTkOptionMenu(self, values=self.cnf_manager.categorias, width=180, variable=self.gvar.categoria,
                      **list_configs).grid(column=0, row=1)

        CTkLabel(self, text='Código do curso', **label_configs).grid(column=1, row=0)
        CTkEntry(self, textvariable=self.gvar.sub_categoria, **entry_configs).grid(column=1, row=1)

        CTkLabel(self, text='Tempo de resposta', **label_configs).grid(column=2, row=0)
        CTkEntry(self, textvariable=self.gvar.tempo, **entry_configs).grid(column=2, row=1)

        CTkLabel(self, text='Tipo da questão', **label_configs).grid(column=0, row=2, pady=(10, 0))
        CTkOptionMenu(self, values=self.cnf_manager.tipos, width=180, variable=self.gvar.tipo,
                      command=self.gvar.altera_tipo_alternativa, **list_configs).grid(column=0, row=3)

        CTkLabel(self, text='Dificuldade', **label_configs).grid(column=1, row=2, pady=(10, 0))
        CTkOptionMenu(self, values=self.cnf_manager.dificuldades, width=180, variable=self.gvar.dificuldade,
                      **list_configs).grid(column=1, row=3)

        CTkLabel(self, text='Peso da questão', **label_configs).grid(column=2, row=2, pady=(10, 0))
        CTkEntry(self, textvariable=self.gvar.peso, **entry_configs).grid(column=2, row=3)
