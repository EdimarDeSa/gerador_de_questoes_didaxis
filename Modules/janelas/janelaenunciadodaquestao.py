from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkOptionMenu, CTkRadioButton, CTkCheckBox
from Modules.configuracoes import *
from Modules.models.caixa_de_texto import *
from Modules.corretor_ortografico import *

from Modules.constants import *

__all__ = ['JanelaEnunciadoDaQuestao']


class JanelaEnunciadoDaQuestao(CTkFrame):
    def __init__(
            self, master: CTk, configs: Configuracoes, var_contador_de_opcoes: int, tipo: CTkOptionMenu,
            var_lista_txt_box: list[CaixaDeTexto], var_lista_rd_bts: list[CTkRadioButton],
            var_lista_ck_bts: list[CTkCheckBox], **kwargs
    ):
        super().__init__(master)

        corretor: CorretorOrtografico = kwargs.get('corretor', None)

        self.var_contador_de_opcoes = var_contador_de_opcoes
        self.tipo = tipo
        self.var_lista_txt_box = var_lista_txt_box
        self.var_lista_rd_bts = var_lista_rd_bts
        self.var_lista_ck_bts = var_lista_ck_bts

        CTkLabel(self, **configs.label_titulos_configs, text='Enunciado da questão').grid(row=0, column=0, padx=20)
        self.pergunta = CaixaDeTexto(self, **configs.text_configs, height=90)
        self.pergunta.grid(row=1, column=0, rowspan=2, padx=10, pady=10, ipadx=260)
        corretor.monitora_textbox(self.pergunta)

        CTkLabel(self, **configs.label_titulos_configs, text='Opção').grid(row=0, column=1)

        self.bt_add_opcao = CTkButton(
            self, **configs.buttons_configs, text='+', width=30, height=30, command=self.add_alternativa
        )
        self.bt_add_opcao.grid(row=1, column=1, padx=10)

        self.bt_rm_opcao = CTkButton(
            self, **configs.buttons_configs, text='-', width=30, height=30, command=self.rm_alternativa
        )
        self.bt_rm_opcao.grid(row=2, column=1, padx=10)

        tipo.configure(command=self.altera_tipo_alternativa)

    def add_alternativa(self, texto_alternativa=None, indice=None):
        if self.var_contador_de_opcoes == 10 or self.tipo.get() == D: return None

        if indice is None: indice = self.var_contador_de_opcoes

        pady = (50 if not indice else 10, 0)

        texto = self.var_lista_txt_box[indice]
        texto.grid(column=0, row=indice, sticky=NSEW, pady=pady)

        if texto_alternativa is not None:
            texto.insert(1.0, texto_alternativa)

        bt = self.get_opcao_bt(indice, self.tipo.get())
        bt.grid(column=1, row=indice, padx=(10, 0), pady=pady)

        self.var_contador_de_opcoes += 1

    def rm_alternativa(self, indice=None):
        if not self.var_contador_de_opcoes: return None

        self.var_contador_de_opcoes -= 1

        if indice is None: indice = self.var_contador_de_opcoes

        texto: CaixaDeTexto = self.var_lista_txt_box[indice]
        texto.grid_forget()

        self.var_lista_ck_bts[indice].grid_forget()
        self.var_lista_rd_bts[indice].grid_forget()

    def altera_tipo_alternativa(self, tipo: str):
        quantidade_de_opcoes = self.var_contador_de_opcoes
        for indice in range(quantidade_de_opcoes):
            self.rm_alternativa(indice=indice)
            self.add_alternativa(indice=indice)
        # self.organiza_ordem_tabulacao()

    def get_opcao_bt(self, indice: int, tipo: str) -> [CTkRadioButton, CTkCheckBox]:
        if tipo == ME:
            return self.get_rd_bt(indice)
        elif tipo == MEN or tipo == VF:
            return self.get_ck_bt(indice)
        else:
            return None

    def get_rd_bt(self, indice) -> CTkRadioButton:
        return self.var_lista_rd_bts[indice]

    def get_ck_bt(self, indice) -> CTkCheckBox:
        return self.var_lista_ck_bts[indice]
