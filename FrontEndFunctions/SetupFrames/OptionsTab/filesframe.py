from customtkinter import CTkFrame, CTkLabel, CTkToplevel, CTkButton

from FrontEndFunctions.Hints import ExportHandler, OpenDbHandler
from FrontEndFunctions.Constants import GRAY


class FilesFrame(CTkFrame):
    def __init__(self, master: CTkToplevel, open_db_handler: OpenDbHandler, export_handler: ExportHandler, **kwargs):
        super().__init__(master, fg_color=GRAY, **kwargs)

        pad = dict(padx=10, pady=10)

        CTkLabel(self, text='Arquivo').grid(row=0, column=0, columnspan=2, pady=(10, 0))

        CTkButton(self, text='Abrir', command=open_db_handler).grid(row=1, column=0, **pad)

        CTkButton(self, text='Criar novo', command=export_handler).grid(row=1, column=1, **pad)
