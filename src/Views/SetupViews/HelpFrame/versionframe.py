from customtkinter import CTkFrame, CTkToplevel, CTkLabel, CTkButton

from src.Hints.hints import MenuSettingsHint


class VersionFrame(CTkFrame):
    def __init__(self, master: CTkToplevel, label_configs: MenuSettingsHint, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=3)

        # TODO: Implementar atualização
        CTkLabel(
            self, text=f'Versão: {self.__class__.__basicsize__}', **label_configs
        ).grid(row=0, column=0)
        CTkButton(self, text='Verificar atualização', command=self).grid(row=0, column=1)
