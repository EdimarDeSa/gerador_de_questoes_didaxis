from customtkinter import CTk, CTkFrame, CTkButton
from Modules.configuracoes import *
from Modules.imagens import *
from Modules.arquivos import *

from Modules.constants import *

__all__ = ['JanelaDeBotoes']


class JanelaDeBotoes(CTkFrame):
    def __init__(
            self, master: CTk, configs: Configuracoes, imagens: Imagens, arquivos: Arquivos,
            **kwargs
    ):
        super().__init__(master)
        self.rowconfigure(0, weight=1)
        self.columnconfigure((1, 2), weight=3)

        self.bt_configs = CTkButton(self, **configs.buttons_configs, text='', width=30, height=30,
                                    image=imagens.bt_configs_img(), command='self.abre_menu_configuracoes')
        self.bt_configs.grid(column=0, row=0, pady=10, padx=5)

        self.bt_exportar = CTkButton(self, **configs.buttons_configs, text='Exportar', width=400, height=30,
                                     command='self.exportar')
        self.bt_exportar.grid(column=1, row=0, pady=10)

        self.bt_salvar = CTkButton(self, **configs.buttons_configs, text='Salvar', width=400, height=30,
                                   command='self.salvar')
        self.bt_salvar.grid(column=2, row=0, pady=10, padx=5)
