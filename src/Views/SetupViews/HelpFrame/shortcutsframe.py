from customtkinter import CTkLabel, CTkScrollableFrame, E, W

from ....Constants import SHORTCUTS
from ....Hints import MenuSettingsHint


class ShortcutsFrame(CTkScrollableFrame):
    def __init__(self, master, label_settings: MenuSettingsHint, **kwargs):
        super().__init__(master, **kwargs)

        for i in range(2):
            self.grid_columnconfigure(i, weight=i + 1)

        pad = dict(padx=2, pady=5)

        for i, (descricao, atalho) in enumerate(SHORTCUTS):
            CTkLabel(self, text=descricao, **label_settings).grid(
                column=0, row=i, sticky=E, **pad
            )

            CTkLabel(self, text=atalho, **label_settings).grid(
                column=1, row=i, sticky=W, **pad
            )
