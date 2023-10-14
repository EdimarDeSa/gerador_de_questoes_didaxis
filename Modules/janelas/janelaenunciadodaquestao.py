from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton
from Modules.configuracoes import *
from Modules.models.caixa_de_texto import CaixaDeTexto

from Modules.constants import *

__all__ = ['JanelaEnunciadoDaQuestao']


class JanelaEnunciadoDaQuestao(CTkFrame):
    def __init__(
            self, master: CTk, configs: Configuracoes, cmd_rm_alternativa=None, cmd_add_alternativa=None,
            **kwargs
    ):
        super().__init__(master)

        CTkLabel(self, **configs.label_titulos_configs, text='Enunciado da questão').grid(row=0, column=0, padx=20)
        self.pergunta = CaixaDeTexto(self, **configs.text_configs, height=90)
        self.pergunta.grid(row=1, column=0, rowspan=2, padx=10, pady=10, ipadx=260)

        CTkLabel(self, **configs.label_titulos_configs, text='Opção').grid(row=0, column=1)
        self.bt_add_opcao = CTkButton(
            self, **configs.buttons_configs, text='+', width=30, height=30, command=cmd_add_alternativa
        )
        self.bt_add_opcao.grid(row=1, column=1, padx=10)
        self.bt_rm_opcao = CTkButton(
            self, **configs.buttons_configs, text='-', width=30, height=30,
            command=cmd_rm_alternativa)
        self.bt_rm_opcao.grid(row=2, column=1, padx=10)
