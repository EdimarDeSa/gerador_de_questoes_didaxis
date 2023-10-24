from customtkinter import CTkScrollableFrame, CTkLabel, E, W

from FrontEndFunctions.Hints import ConfigsHint
from FrontEndFunctions.Constants import SHORTCUTS


class ShortcutsFrame(CTkScrollableFrame):
    def __init__(self, master, label_configs: ConfigsHint, **kwargs):
        super().__init__(master, **kwargs)
        for i in range(2): self.grid_columnconfigure(i, weight=i+1)

        pad = dict(padx=2, pady=5)

        for i, (descricao, atalho) in enumerate(SHORTCUTS):
            CTkLabel(self, text=descricao, **label_configs).grid(column=0, row=i, sticky=E, **pad)
            CTkLabel(self, text=atalho, **label_configs).grid(column=1, row=i, sticky=W, **pad)
