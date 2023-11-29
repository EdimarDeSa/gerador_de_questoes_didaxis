from customtkinter import CTk, CTkFrame, CTkLabel, N, S, Variable

from ..Hints import MenuSettingsHint


class QuestionCountFrame(CTkFrame):
    def __init__(
        self,
        master: CTk,
        label_settings: MenuSettingsHint,
        question_count: Variable,
    ):
        super().__init__(master)

        CTkLabel(self, text='Total de questões:', **label_settings, wraplength=85).pack(
            anchor=S, expand=True
        )

        CTkLabel(self, textvariable=question_count, **label_settings).pack(
            anchor=N, expand=True
        )
