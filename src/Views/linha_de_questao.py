from tkinter.messagebox import askyesno

from customtkinter import CTkButton, CTkFrame, CTkImage, CTkLabel, StringVar, W

from src.Constants import BORDER_BLUE
from src.Hints import Callable


class LinhaDeQuestao:
    def __init__(
        self,
        master: CTkFrame,
        title: str,
        controle: int,
        img_edit: CTkImage,
        img_delete: CTkImage,
        cmd_edit: Callable,
        cmd_delete: Callable,
        **kwargs
    ):
        self.controle = controle
        self.title = StringVar(value=title)

        self.cmd_edit = cmd_edit
        self.cmd_delete = cmd_delete
        border = dict(
            border_width=1, border_spacing=1, border_color=BORDER_BLUE
        )

        CTkLabel(
            master, textvariable=self.title, anchor=W, wraplength=540
        ).place(relx=0.01, relwidth=0.8, relheight=1)

        CTkButton(
            master,
            text=None,
            command=self._botao_editar,
            image=img_edit,
            **border
        ).place(relx=0.815, rely=0.05, relwidth=0.06, relheight=0.9)

        CTkButton(
            master,
            text=None,
            command=self._botao_deletar,
            image=img_delete,
            **border
        ).place(relx=0.915, rely=0.05, relwidth=0.06, relheight=0.9)

    def _botao_deletar(self):
        resposta = askyesno(
            'Deseja deletar a questão?',
            'Tem certeza que deseja deletar a questão? Esse processo não poderá ser desfeito.',
        )

        if resposta:
            self.cmd_delete(self.controle)

    def _botao_editar(self):
        self.cmd_edit(self.controle)
