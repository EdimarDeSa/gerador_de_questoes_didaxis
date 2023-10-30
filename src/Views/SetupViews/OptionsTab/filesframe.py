from customtkinter import CTkFrame, CTkLabel, CTkToplevel, CTkButton

from src.Hints import Callable, MenuSettingsHint


class FilesFrame(CTkFrame):
    def __init__(
        self,
        master: CTkToplevel,
        label_settings: MenuSettingsHint,
        button_settings: MenuSettingsHint,
        new_db_handler: Callable,
        open_db_handler: Callable,
        export_as_db_handler: Callable,
        **kwargs
    ):
        super().__init__(master, **kwargs)

        pad = dict(padx=5, pady=5)

        CTkLabel(self, text="Arquivos", **label_settings).grid(
            row=0, column=0, columnspan=2, pady=(10, 0)
        )

        CTkButton(self, text="Novo", command=new_db_handler, **button_settings).grid(
            row=1, column=0, **pad
        )

        CTkButton(self, text="Abrir", command=open_db_handler, **button_settings).grid(
            row=1, column=1, **pad
        )

        CTkButton(
            self, text="Salvar como", command=export_as_db_handler, **button_settings
        ).grid(column=0, columnspan=2, row=2, **pad)
