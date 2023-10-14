from customtkinter import CTkFrame, CTk, CTkLabel, StringVar
from Modules.configuracoes import *


__all__ = ['JanelaQuantidadeDeQuestoes']


class JanelaQuantidadeDeQuestoes(CTkFrame):
    def __init__(self, master: CTk, configs: Configuracoes, var: StringVar, **kwargs):
        super().__init__(master)

        CTkLabel(self, textvariable=var, **configs.label_titulos_configs, wraplength=85).pack(expand=True)

