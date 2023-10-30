from customtkinter import (
    CTkScrollableFrame,
    CTkToplevel,
    CTkRadioButton,
    BOTH,
    Variable,
)

from src.Hints import Callable, MenuSettingsHint, List


class CategorySelectionFrame(CTkScrollableFrame):
    def __init__(
        self,
        master: CTkToplevel,
        button_default_settings: MenuSettingsHint,
        category_list: List,
        categoria: Variable,
        categori_change_handler: Callable,
        **kwargs
    ):
        super().__init__(master, label_text="Unidade padrão", **kwargs)

        for indice, unidade in enumerate(category_list):
            CTkRadioButton(
                self,
                text=unidade,
                value=unidade,
                variable=categoria,
                command=categori_change_handler,
                **button_default_settings
            ).pack(ipadx=10, pady=(0, 5), fill=BOTH)
