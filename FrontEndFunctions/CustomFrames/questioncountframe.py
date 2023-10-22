from customtkinter import CTk, CTkFrame, CTkLabel, S, N

from ..Hints import ConfigsHint, IntVarHint


class QuestionCountFrame(CTkFrame):
    def __init__(
            self, master: CTk, label_configs: ConfigsHint, display_question_count: IntVarHint, **kwargs
    ):
        super().__init__(master, **kwargs)

        CTkLabel(self, text='Total de questões:', **label_configs, wraplength=85).pack(anchor=S, expand=True)

        CTkLabel(self, textvariable=display_question_count, **label_configs).pack(anchor=N, expand=True)

