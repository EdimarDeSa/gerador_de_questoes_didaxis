from customtkinter import CTkFrame, CTk, CTkLabel, CTkEntry, CTkOptionMenu, StringVar
from Modules.configuracoes import *

from Modules.constants import *

__all__ = ['JanelaParametrosDaQuestao']


class JanelaParametrosDaQuestao(CTkFrame):
    def __init__(
            self, master: CTk, configs: Configuracoes, var_unidade_padrao: StringVar,
            **kwargs
    ):
        super().__init__(master)

        CTkLabel(self, **configs.label_titulos_configs, text='Unidade').grid(column=0, row=0, padx=20)
        self.unidade = CTkOptionMenu(
            self, **configs.list_configs, values=configs.unidades, width=165, dynamic_resizing=False,
            variable=var_unidade_padrao
        )
        self.unidade.grid(column=0, row=1, padx=20, pady=(0, 20))

        CTkLabel(self, **configs.label_titulos_configs, text='Código do curso').grid(column=1, row=0, padx=20)
        self.codigo_do_curso = CTkEntry(self, **configs.entry_configs, placeholder_text=PLACE_HOLDER_CODIGO)
        self.codigo_do_curso.grid(column=1, row=1, padx=20, pady=(0, 20))

        CTkLabel(self, **configs.label_titulos_configs, text='Tempo de resposta').grid(column=2, row=0, padx=20)
        self.tempo = CTkEntry(self, **configs.entry_configs, placeholder_text=PLACE_HOLDER_TEMPO)
        self.tempo.grid(column=2, row=1, padx=20, pady=(0, 20))

        CTkLabel(self, **configs.label_titulos_configs, text='Tipo da questão').grid(column=0, row=2, padx=20)
        self.tipo = CTkOptionMenu(self, **configs.list_configs, values=configs.tipos, width=165, dynamic_resizing=False)
        self.tipo.grid(column=0, row=3, padx=20, pady=(0, 20))
        self.tipo.set(configs.tipos[1])

        CTkLabel(self, **configs.label_titulos_configs, text='Dificuldade').grid(column=1, row=2, padx=20)
        self.dificuldade = CTkOptionMenu(
            self, **configs.list_configs, values=configs.dificuldades, dynamic_resizing=False)
        self.dificuldade.grid(column=1, row=3, padx=20, pady=(0, 20))

        CTkLabel(self, **configs.label_titulos_configs, text='Peso da questão').grid(column=2, row=2, padx=20)
        self.peso = CTkEntry(self, **configs.entry_configs, placeholder_text=PLACE_HOLDER_PESO)
        self.peso.grid(column=2, row=3, padx=20, pady=(0, 20))
