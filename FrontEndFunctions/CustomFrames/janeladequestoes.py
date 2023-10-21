from customtkinter import CTk, CTkFrame, CTkLabel, CTkScrollableFrame, CTkImage, BOTH, X

from ..Hints import ConfigsHint, ImageHint, RowHint
from ..Constants import VERDE


class JanelaDeQuestoes(CTkFrame):
    def __init__(
            self, master: CTk, label_configs: ConfigsHint, img_edit: ImageHint, img_delete: ImageHint,
            **kwargs
    ):
        super().__init__(master, **kwargs)

        self.label_configs = label_configs
        self.img_edit = img_edit
        self.img_delete = img_delete

        self._master: CTkScrollableFrame = CTkScrollableFrame(self)
        self._master.pack(fill=BOTH, expand=True)

        self._row_dict: RowHint = dict()
        self._zebrar: bool = True
        self._linha_atual: int = 0

        self._init_header()

    def _init_header(self):
        fg_label_configs = self.label_configs.copy()
        fg_label_configs.update({'fg_color': VERDE})

        bg_label_configs = self.label_configs.copy()
        bg_label_configs.update({'bg_color': VERDE})

        frame = CTkFrame(self._master, fg_color=VERDE, height=45)
        frame.pack(expand=True, fill=X)

        CTkLabel(frame, text='Enunciado', **fg_label_configs).place(relx=0.01, relwidth=0.8, relheight=1)
        CTkLabel(frame, text='Editar', **bg_label_configs).place(relx=0.8, relwidth=0.09, relheight=1)
        CTkLabel(frame, text='Deletar', **bg_label_configs).place(relx=0.9, relwidth=0.09, relheight=1)
