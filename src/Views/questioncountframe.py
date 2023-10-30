from customtkinter import CTk, CTkFrame, CTkLabel
from customtkinter import S, N, Variable

from src.Hints import MenuSettingsHint


class QuestionCountFrame(CTkFrame):
    def __init__(
        self,
        master: CTk,
        label_configs: MenuSettingsHint,
        display_question_count: Variable,
    ):
        super().__init__(master)

        CTkLabel(self, text="Total de questões:", **label_configs, wraplength=85).pack(
            anchor=S, expand=True
        )

        CTkLabel(self, textvariable=display_question_count, **label_configs).pack(
            anchor=N, expand=True
        )
