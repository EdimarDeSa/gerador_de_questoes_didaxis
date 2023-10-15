from customtkinter import CTk, CTkFrame, CTkButton, StringVar, BooleanVar
from Modules.configuracoes import *
from Modules.imagens import *
from Modules.arquivos import *
from Modules.perfil import *

from Modules.painel_de_configuracoes import *

from Modules.constants import *

__all__ = ['JanelaDeBotoes']


class JanelaDeBotoes(CTkFrame):
    def __init__(
            self, master: CTk, configs: Configuracoes, imagens: Imagens, arquivos: Arquivos, perfil: Perfil,
            var_unidade_padrao: StringVar, var_apagar_enunciado: BooleanVar, var_dark_mode: StringVar,
            var_escala_do_sistema: StringVar,
            **kwargs
    ):
        super().__init__(master)

        self.configs = configs
        self.arquivos = arquivos
        self.perfil = perfil
        self.var_unidade_padrao = var_unidade_padrao
        self.var_apagar_enunciado = var_apagar_enunciado
        self.var_dark_mode = var_dark_mode
        self.var_escala_do_sistema = var_escala_do_sistema

        self.columnconfigure((1, 2), weight=3)

        self.bt_configs = CTkButton(self, **configs.buttons_configs, text=None, width=32, height=32,
                                    image=imagens.bt_configs_img(), command=self.abre_menu_configuracoes)
        self.bt_configs.grid(column=0, row=0, pady=10, padx=5)

        self.bt_exportar = CTkButton(self, **configs.buttons_configs, text='Exportar', height=32,
                                     command='self.exportar')
        self.bt_exportar.grid(column=1, row=0, pady=10, sticky=NSEW)

        self.bt_salvar = CTkButton(self, **configs.buttons_configs, text='Salvar', height=32,
                                   command='self.salvar')
        self.bt_salvar.grid(column=2, row=0, pady=10, padx=5, sticky=NSEW)

    def abre_menu_configuracoes(self):
        # if self.children.get(''):
        #     return self.painel_de_configuracoes.focus_force()
        self.painel_de_configuracoes = PainelDeConfiguracoes(
            self, self.configs, self.perfil, self.var_unidade_padrao, self.var_apagar_enunciado, self.var_dark_mode,
            self.var_escala_do_sistema
        )
        print(self.winfo_children())
