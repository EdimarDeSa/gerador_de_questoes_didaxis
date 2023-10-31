from customtkinter import CTk, CTkButton, CTkFrame, CTkLabel, CTkTextbox

from src.Hints import Callable, MenuSettingsHint


class QuestionStatementFrame(CTkFrame):
    def __init__(
        self,
        master: CTk,
        label_configs: MenuSettingsHint,
        entry_configs: MenuSettingsHint,
        button_configs: MenuSettingsHint,
        add_choice_handler: Callable,
        rm_choice_handler: Callable,
    ):
        super().__init__(master)

        button_configs = button_configs.copy()
        button_configs.update({'width': 30, 'height': 30})

        CTkLabel(self, text='Enunciado da questão', **label_configs).place(
            relx=0.02, rely=0.025, relwidth=0.85
        )
        self.question = CTkTextbox(self, **entry_configs, height=90)
        self.question.place(relx=0.02, rely=0.25, relwidth=0.85, relheight=0.7)

        CTkLabel(self, text='Opção', **label_configs).place(
            relx=0.85, rely=0.025, relwidth=0.15
        )
        CTkButton(
            self, text='+', command=add_choice_handler, **button_configs
        ).place(relx=0.905, rely=0.35)
        CTkButton(
            self, text='-', command=rm_choice_handler, **button_configs
        ).place(relx=0.905, rely=0.65)
