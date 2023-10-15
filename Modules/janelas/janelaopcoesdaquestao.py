from customtkinter import CTk, CTkFrame, CTkLabel, CTkRadioButton, CTkCheckBox, IntVar, CTkScrollableFrame
from Modules.configuracoes import *
from Modules.models.caixa_de_texto import CaixaDeTexto
from Modules.corretor_ortografico import CorretorOrtografico

from Modules.constants import *

__all__ = ['JanelaOpcoesDaQuestao']


class JanelaOpcoesDaQuestao(CTkScrollableFrame):
    def __init__(
            self, master: CTk, configs: Configuracoes, var_opcao_rd_bt: IntVar,  lista_txt_box: list,
            lista_rd_bts: list, lista_ck_bts: list, **kwargs
    ):
        super().__init__(master)
        corretor: CorretorOrtografico = kwargs['corretor']

        CTkLabel(self, text=None).grid(row=0, column=0)
        CTkLabel(self, text='Opções', **configs.label_titulos_configs).place(relx=0.47, rely=0.01)
        self.grid_columnconfigure(0, minsize=800)

        for index in range(10):
            texto = CaixaDeTexto(self, **configs.text_configs, height=50)
            corretor.monitora_textbox(texto)
            lista_txt_box.append(texto)

            rd_button = CTkRadioButton(self, text=None, value=index, variable=var_opcao_rd_bt)
            lista_rd_bts.append(rd_button)

            ck_button = CTkCheckBox(self, text=None)
            lista_ck_bts.append(ck_button)
