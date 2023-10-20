from tkinter.messagebox import askyesno

from customtkinter import CTkFrame, CTkImage, CTkLabel, W, CTkButton, StringVar

from Modules.models.globalvars import *


class LinhaDeQuestao:
    def __init__(self, master: CTkFrame, title: str, controle: int, img_edit: CTkImage, img_delete: CTkImage, **kwargs):
        self.controle = controle
        self.title = StringVar(value=title)

        self.cmd_edit = kwargs.get('cmd_edit')
        self.cmd_delete = kwargs.get('cmd_delete')

        CTkLabel(master, textvariable=self.title, anchor=W,
                 wraplength=540).place(relx=0.01, relwidth=0.8, relheight=1)

        CTkButton(master, text=None, command=self._botao_editar,
                  image=img_edit).place(relx=0.815, rely=0.05, relwidth=0.06, relheight=0.9)

        CTkButton(master, text=None, command=self._botao_deletar,
                  image=img_delete).place(relx=0.915, rely=0.05, relwidth=0.06, relheight=0.9)

    def _botao_deletar(self):
        resposta = askyesno('Deseja deletar a questão?',
                            'Tem certeza que deseja deletar a questão? Esse processo não poderá ser desfeito.')

        if resposta:
            self.cmd_delete(self.controle)

    def _botao_editar(self):
        self.cmd_edit(self.controle)
