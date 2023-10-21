from customtkinter import CTkFrame, CTk, CTkLabel, CTkScrollableFrame, CTkRadioButton, CTkCheckBox

from ..Hints import ConfigsHint, StartMonitorHandler, IntVarHint, ListHint
from FrontEndFunctions.caixa_de_texto import CaixaDeTexto


class JanelaOpcoesDaQuestao(CTkFrame):
    def __init__(
            self, master: CTk, label_configs: ConfigsHint, text_configs: ConfigsHint, var_rd_button_value: IntVarHint,
            start_monitor_handler: StartMonitorHandler, lista_txt_box: ListHint, lista_rd_bts: ListHint,
            lista_ck_bts: ListHint, **kwargs
    ):
        super().__init__(master, **kwargs)

        CTkLabel(self, text='Opções', **label_configs).place(rely=0.02, relwidth=1)

        sc_frame = CTkScrollableFrame(self)
        sc_frame.place(rely=0.12, relwidth=1, relheight=0.88)

        for index in range(10):
            sc_frame.grid_rowconfigure(index, weight=1)

            texto = CaixaDeTexto(sc_frame, width=650, height=50, **text_configs)
            start_monitor_handler(texto)
            lista_txt_box.append(texto)

            rd_button = CTkRadioButton(sc_frame, text=None, value=index, variable=var_rd_button_value)
            lista_rd_bts.append(rd_button)

            ck_button = CTkCheckBox(sc_frame, text=None)
            lista_ck_bts.append(ck_button)
