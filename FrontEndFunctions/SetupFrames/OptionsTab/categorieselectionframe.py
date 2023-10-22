from customtkinter import CTkScrollableFrame, CTkToplevel, CTkRadioButton, BOTH, CTkFrame

from FrontEndFunctions.Constants import GRAY


class CategorieSelectionFrame(CTkScrollableFrame):
    def __init__(self, master: CTkToplevel, category_list, categoria, categori_change_handler, **kwargs):
        super().__init__(master, fg_color=GRAY, label_text='Unidade padrão', **kwargs)

        for indice, unidade in enumerate(category_list):
            CTkRadioButton(
                self, text=unidade, value=unidade, variable=categoria, command=categori_change_handler
            ).pack(ipadx=10, pady=(0, 5), fill=BOTH)
