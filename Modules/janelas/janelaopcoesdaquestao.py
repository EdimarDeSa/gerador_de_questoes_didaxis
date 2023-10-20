from customtkinter import CTkFrame, CTk, CTkLabel, CTkScrollableFrame, CTkRadioButton, CTkCheckBox, BOTH

from ..models.globalvars import *
from ..models.caixa_de_texto import CaixaDeTexto


class JanelaOpcoesDaQuestao(CTkFrame):
    def __init__(self, master: CTk, variaveis_globais: VariaveisGlobais, **kwargs):
        super().__init__(master, **kwargs)

        self.gvar = variaveis_globais

        sc_frame = CTkScrollableFrame(self)
        sc_frame.pack(expand=True, fill=BOTH)

        CTkLabel(sc_frame, text=None).grid(row=0, column=0)
        CTkLabel(sc_frame, text='Opções', **self.gvar.configs.label_titulos_configs).place(relx=0.47, rely=0.01)

        for index in range(10):
            texto = CaixaDeTexto(sc_frame, width=650, height=50, **self.gvar.configs.text_configs)
            self.gvar.corretor_ortografico.monitora_textbox(texto)
            self.gvar.lista_txt_box.append(texto)

            rd_button = CTkRadioButton(sc_frame, text=None, value=index, variable=self.gvar.opcao_correta_radio_bt)
            self.gvar.lista_rd_bts.append(rd_button)

            ck_button = CTkCheckBox(sc_frame, text=None)
            self.gvar.lista_ck_bts.append(ck_button)
