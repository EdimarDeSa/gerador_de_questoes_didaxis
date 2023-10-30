from customtkinter import CTk, CTkFrame, CTkLabel, CTkScrollableFrame, CTkImage, X

from src.Hints import MenuSettingsHint
from src.Constants import GREEN


class QuestionsFrame(CTkScrollableFrame):
    def __init__(
        self,
        master: CTk,
        label_configs: MenuSettingsHint,
        img_edit: CTkImage,
        img_delete: CTkImage,
        **kwargs
    ):
        super().__init__(master, **kwargs)

        # TODO: Cabecalho com problemas em telas grandes, melhorar responsividade

        self.label_configs = label_configs
        self.img_edit = img_edit
        self.img_delete = img_delete

        self._init_header()

    def _init_header(self) -> None:
        fg_label_configs = self.label_configs.copy()
        fg_label_configs["fg_color"] = GREEN

        bg_label_configs = self.label_configs.copy()
        bg_label_configs["bg_color"] = GREEN

        frame = CTkFrame(self, fg_color=GREEN, height=45)
        frame.pack(expand=True, fill=X)

        frame.grid_columnconfigure(0, weight=10)
        for i in range(1, 3):
            frame.grid_columnconfigure(i, weight=1)

        CTkLabel(frame, text="Enunciado", height=40, **fg_label_configs).grid(
            column=0, row=0
        )
        CTkLabel(frame, text="Editar", height=40, **bg_label_configs).grid(
            column=1, row=0
        )
        CTkLabel(frame, text="Deletar", height=40, **bg_label_configs).grid(
            column=2, row=0
        )
