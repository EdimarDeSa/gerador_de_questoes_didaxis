from customtkinter import CTkFrame, CTk, CTkLabel, CTkScrollableFrame, CTkRadioButton, CTkCheckBox, Variable, CTkTextbox

from .Hints import MenuSettingsHint, WidgetListHint


class QuestionChoicesFrame(CTkFrame):
    def __init__(
            self, master: CTk,
            label_configs: MenuSettingsHint, text_configs: MenuSettingsHint, var_rd_button_value: Variable,
            lista_txt_box: WidgetListHint, lista_rd_bts: WidgetListHint, lista_ck_bts: WidgetListHint
    ):
        super().__init__(master)

        CTkLabel(self, text='Opções', **label_configs).place(rely=0.02, relwidth=1)

        sc_frame = CTkScrollableFrame(self)
        sc_frame.place(rely=0.12, relwidth=1, relheight=0.88)

        for index in range(10):
            sc_frame.grid_rowconfigure(index, weight=1)

            texto = CTkTextbox(sc_frame, width=650, height=50, **text_configs)
            lista_txt_box.append(texto)

            rd_button = CTkRadioButton(sc_frame, text=None, value=index, variable=var_rd_button_value)
            lista_rd_bts.append(rd_button)

            ck_button = CTkCheckBox(sc_frame, text=None)
            lista_ck_bts.append(ck_button)
