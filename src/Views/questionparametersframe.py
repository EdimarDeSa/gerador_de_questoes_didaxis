from customtkinter import CTk, CTkEntry, CTkFrame, CTkLabel, CTkOptionMenu, Variable

from src.Hints import MenuSettingsHint


class QuestionParametersFrame(CTkFrame):
    def __init__(
        self,
        master: CTk,
        label_settings: MenuSettingsHint,
        entry_settings: MenuSettingsHint,
        category_settings: MenuSettingsHint,
        subcategory: Variable,
        deadline: Variable,
        question_type_settings: MenuSettingsHint,
        difficulty_settings: MenuSettingsHint,
        question_weight: Variable,
    ):
        super().__init__(master)
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)

        CTkLabel(self, **label_settings, text='Unidade').grid(column=0, row=0)
        CTkOptionMenu(self, **category_settings).grid(column=0, row=1)

        CTkLabel(self, text='Código do curso', **label_settings).grid(column=1, row=0)
        CTkEntry(self, textvariable=subcategory, **entry_settings).grid(column=1, row=1)

        CTkLabel(self, text='Tempo de resposta', **label_settings).grid(column=2, row=0)
        CTkEntry(self, textvariable=deadline, **entry_settings).grid(column=2, row=1)

        CTkLabel(self, text='Tipo da questão', **label_settings).grid(
            column=0, row=2, pady=(10, 0)
        )
        CTkOptionMenu(self, **question_type_settings).grid(column=0, row=3)

        CTkLabel(self, text='Dificuldade', **label_settings).grid(
            column=1, row=2, pady=(10, 0)
        )
        CTkOptionMenu(self, **difficulty_settings).grid(column=1, row=3)

        CTkLabel(self, text='Peso da questão', **label_settings).grid(
            column=2, row=2, pady=(10, 0)
        )
        CTkEntry(
            self,
            validate='key',
            validatecommand=(self.register(self._only_numbers), '%P'),
            textvariable=question_weight,
            **entry_settings
        ).grid(column=2, row=3)

    def _only_numbers(self, digit: str) -> bool:
        return digit.isdigit()
