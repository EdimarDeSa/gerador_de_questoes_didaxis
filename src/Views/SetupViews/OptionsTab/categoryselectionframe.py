from customtkinter import (
    BOTH,
    CTkRadioButton,
    CTkScrollableFrame,
    CTkToplevel,
    Variable,
)

from src.Hints import Callable, List, MenuSettingsHint


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
        super().__init__(master, label_text='Unidade padrão', **kwargs)

        for unidade in category_list:
            CTkRadioButton(
                self,
                text=unidade,
                value=unidade,
                variable=categoria,
                command=categori_change_handler,
                **button_default_settings
            ).pack(ipadx=10, pady=(0, 5), fill=BOTH)
