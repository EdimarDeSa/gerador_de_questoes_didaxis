from customtkinter import CTkFrame, CTk, CTkLabel, CTkOptionMenu, CTkEntry

from ..models.globalvars import VariaveisGlobais
from ..constants import PLACE_HOLDER_PESO, PLACE_HOLDER_CODIGO, PLACE_HOLDER_TEMPO


class JanelaParametrosDaQuestao(CTkFrame):
    def __init__(self, master: CTk, variaveis_globais: VariaveisGlobais, **kwargs):
        super().__init__(master, **kwargs)

        self.gvar = variaveis_globais

        CTkLabel(self, **self.gvar.cnf_manager.label_titulos_configs, text='Unidade').grid(column=0, row=0, padx=20)
        self.unidade = CTkOptionMenu(self, values=self.gvar.cnf_manager.unidades, width=165, dynamic_resizing=False,
                                     variable=self.gvar.var_unidade_padrao, **self.gvar.cnf_manager.list_configs)
        self.unidade.grid(column=0, row=1, padx=20, pady=(0, 20))

        CTkLabel(self, text='Código do curso',
                 **self.gvar.cnf_manager.label_titulos_configs).grid(column=1, row=0, padx=20)
        self.codigo_do_curso = CTkEntry(self, placeholder_text=PLACE_HOLDER_CODIGO,
                                        **self.gvar.cnf_manager.entry_configs)
        self.codigo_do_curso.grid(column=1, row=1, padx=20, pady=(0, 20))

        CTkLabel(self, text='Tempo de resposta',
                 **self.gvar.cnf_manager.label_titulos_configs).grid(column=2, row=0, padx=20)
        self.tempo = CTkEntry(self, placeholder_text=PLACE_HOLDER_TEMPO, **self.gvar.cnf_manager.entry_configs)
        self.tempo.grid(column=2, row=1, padx=20, pady=(0, 20))

        CTkLabel(self, text='Tipo da questão',
                 **self.gvar.cnf_manager.label_titulos_configs).grid(column=0, row=2, padx=20)
        self.tipo = CTkOptionMenu(self, values=self.gvar.cnf_manager.tipos, width=165, dynamic_resizing=False,
                                  **self.gvar.cnf_manager.list_configs)
        self.tipo.grid(column=0, row=3, padx=20, pady=(0, 20))
        self.tipo.set(self.gvar.cnf_manager.tipos[1])

        CTkLabel(self, text='Dificuldade', **self.gvar.cnf_manager.label_titulos_configs).grid(column=1, row=2, padx=20)
        self.dificuldade = CTkOptionMenu(self, values=self.gvar.cnf_manager.dificuldades, dynamic_resizing=False,
                                         **self.gvar.cnf_manager.list_configs)
        self.dificuldade.grid(column=1, row=3, padx=20, pady=(0, 20))

        CTkLabel(self, text='Peso da questão',
                 **self.gvar.cnf_manager.label_titulos_configs).grid(column=2, row=2, padx=20)
        self.peso = CTkEntry(self, placeholder_text=PLACE_HOLDER_PESO, **self.gvar.cnf_manager.entry_configs)
        self.peso.grid(column=2, row=3, padx=20, pady=(0, 20))
        
        # ------ Adiciona variáveis globais ------ #

        self.gvar.unidade = self.unidade
        self.gvar.codigo_do_curso = self.codigo_do_curso
        self.gvar.tempo = self.tempo
        self.gvar.tipo = self.tipo
        self.gvar.dificuldade = self.dificuldade
        self.gvar.peso = self.peso
