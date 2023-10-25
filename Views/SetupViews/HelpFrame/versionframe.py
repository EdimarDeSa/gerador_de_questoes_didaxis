from customtkinter import CTkFrame, CTkToplevel, CTkLabel, CTkButton, CENTER, BOTH

from FrontEndFunctions.Hints import ConfigsHint
from setuptools_scm import get_version
import __main__


class VersionFrame(CTkFrame):
    def __init__(self, master: CTkToplevel, label_configs: ConfigsHint, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=3)

        # TODO: Implementar atualização
        CTkLabel(
            self, text=f'Versão: {get_version(relative_to=__main__.__file__)}', **label_configs
        ).grid(row=0, column=0)
        CTkButton(self, text='Verificar atualização', command='self.verifica_atualizacao').grid(row=0, column=1)
