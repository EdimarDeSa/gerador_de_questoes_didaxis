from customtkinter import CTk, CTkFrame, CTkLabel, CTkRadioButton, CTkCheckBox
from Modules.configuracoes import *
from Modules.models.caixa_de_texto import CaixaDeTexto
from Modules.corretor_ortografico import CorretorOrtografico

from Modules.constants import *

__all__ = ['JanelaOpcoesDaQuestao']


class JanelaOpcoesDaQuestao(CTkFrame):
    def __init__(
            self, master: CTk, configs: Configuracoes, var_opcao_rd_bt, var_contador_op,
            **kwargs
    ):
        super().__init__(master)

        corretor: CorretorOrtografico = kwargs['corretor']

        CTkLabel(self, text='Opções', **configs.label_titulos_configs).place(relx=0.47, rely=0.01)

        for index in range(10):
            texto = CaixaDeTexto(self, **configs.text_configs, height=50)
            setattr(self, f'txt_opcao{index}', texto)
            corretor.monitora_textbox(texto)

            rd_button = CTkRadioButton(self, text='', value=index, variable=var_opcao_rd_bt)
            setattr(self, f'rd_button_opcao{index}', rd_button)

            ck_button = CTkCheckBox(self, text='')
            setattr(self, f'ck_button_opcao{index}', ck_button)