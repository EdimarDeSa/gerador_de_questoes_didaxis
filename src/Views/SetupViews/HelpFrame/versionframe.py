from customtkinter import CTkButton, CTkFrame, CTkLabel, CTkToplevel

from src.Hints.hints import Callable, MenuSettingsHint


class VersionFrame(CTkFrame):
    def __init__(
        self,
        master: CTkToplevel,
        label_configs: MenuSettingsHint,
        get_version: Callable,
        version: str,
        **kwargs,
    ):
        super().__init__(master, **kwargs)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=3)

        # TODO: Implementar atualização
        CTkLabel(self, text=f'Versão: {version}', **label_configs).grid(
            row=0, column=0
        )

        CTkButton(self, text='Verificar atualização', command=get_version).grid(
            row=0, column=1
        )