from customtkinter import CTkFrame, CTk, CTkLabel, CTkScrollableFrame, CTkRadioButton, CTkCheckBox, BOTH

from ..configuration_manager import ConfigurationManager
from ..models.globalvars import VariaveisGlobais
from ..models.caixa_de_texto import CaixaDeTexto


class JanelaOpcoesDaQuestao(CTkFrame):
    def __init__(self, master: CTk, configuration_manager: ConfigurationManager, variaveis_globais: VariaveisGlobais,
                 **kwargs):
        super().__init__(master, **kwargs)

        self.cnf_manager = configuration_manager
        self.gvar = variaveis_globais

        CTkLabel(self, text='Opções', **self.cnf_manager.label_titulos_configs).place(rely=0.02, relwidth=1)

        sc_frame = CTkScrollableFrame(self)
        sc_frame.place(rely=0.12, relwidth=1, relheight=0.88)

        for index in range(10):
            sc_frame.grid_rowconfigure(index, weight=1)

            texto = CaixaDeTexto(sc_frame, width=650, height=50, **self.cnf_manager.text_configs)
            self.gvar.corretor_ortografico.monitora_textbox(texto)
            self.gvar.lista_txt_box.append(texto)

            rd_button = CTkRadioButton(sc_frame, text=None, value=index, variable=self.gvar.opcao_correta_radio_bt)
            self.gvar.lista_rd_bts.append(rd_button)

            ck_button = CTkCheckBox(sc_frame, text=None)
            self.gvar.lista_ck_bts.append(ck_button)
