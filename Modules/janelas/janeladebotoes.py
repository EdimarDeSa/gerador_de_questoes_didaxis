from tkinter.messagebox import showwarning, showinfo

from customtkinter import CTkFrame, CTk, CTkButton, NSEW, CTkCheckBox, CTkRadioButton, CTkImage

from ..configuration_manager import ConfigurationManager
from ..models.globalvars import VariaveisGlobais
from ..models.caixa_de_texto import CaixaDeTexto
from ..constants import D, ME, MEN, VF


class JanelaDeBotoes(CTkFrame):
    def __init__(self, master: CTk, configuration_manager: ConfigurationManager, variaveis_globais: VariaveisGlobais,
                 img_config: CTkImage, **kwargs):
        super().__init__(master, **kwargs)

        self.cnf_manager = configuration_manager
        self.gvar = variaveis_globais

        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=3)

        # noinspection PyTypeChecker
        CTkButton(
            self, text=None, width=60, height=32, image=img_config,
            command=self.abre_menu_configuracoes, **self.cnf_manager.buttons_configs
        ).pack(expand=True, side='left')
        CTkButton(
            self, text='Exportar', width=300, height=32, command='self.exportar', **self.cnf_manager.buttons_configs
        ).pack(expand=True, side='left', fill='x', padx=(0, 10))

        self.bt_salvar = CTkButton(
            self, text='Salvar', width=300, height=32, command='self.salvar_questao', **self.cnf_manager.buttons_configs
        )
        self.bt_salvar.pack(expand=True, side='left', fill='x', padx=(0, 10))

        # ------ Adiciona variáveis globais ------ #

        self.gvar.exportar = 'self.exportar'

    def abre_menu_configuracoes(self):
        painel = self.children.get('!paineldeconfiguracoes')
        if painel: return painel.focus_force()

        # PainelDeConfiguracoes(self, self.gvar)

    # def salvar_questao(self):
    #     if not self.gvar.pergunta.get_texto_completo() or self.verifica_texto_opcoes():
    #         return showwarning(
    #             'Pergunta em branco',
    #             'Para salvar uma questão é necessário que a pergunta e as np_alternativas ativas não esteja em '
    #             'branco.'
    #         )
    #
    #     if self.gvar.questao_em_edicao:
    #         self.salvar_edicao()
    #         return
    #
    #     if self.gvar.quadro_de_questoes.verifica_se_pergunta_ja_existe():
    #         return showinfo('Pergunta repetida', 'Já existe uma questão com a mesma pergunta')
    #
    #     questao = ModeloQuestao(
    #         self.gvar.unidade.get(), self.gvar.sub_categoria.get(), self.gvar.tempo.get(),
    #         self.gvar.tipo.get(), self.gvar.dificuldade.get(), self.gvar.peso.get(),
    #         self.gvar.pergunta.get_texto_completo(), self.get_opcoes()
    #     )
    #     self.gvar.quadro_de_questoes.adiciona_questao(questao)
    #
    #     self.gvar.reseta_informacoes()
    #     self.gvar.exportado = False

    # def verifica_texto_opcoes(self):
    #     if self.gvar.tipo.get() != D:
    #         if not self.gvar.contador_de_opcoes.get():
    #             return True
    #         for indice in range(self.gvar.contador_de_opcoes.get()):
    #             opcao: CaixaDeTexto = self.gvar.lista_txt_box[indice]
    #             if not opcao.get_texto_completo():
    #                 return True
    #     return False

    # def salvar_edicao(self):
    #     self.gvar.questao_em_edicao.categoria = self.gvar.unidade.get()
    #     self.gvar.questao_em_edicao.subcategoria = self.gvar.sub_categoria.get()
    #     self.gvar.questao_em_edicao.tempo = self.gvar.tempo.get()
    #     self.gvar.questao_em_edicao.tipo = self.gvar.tipo.get()
    #     self.gvar.questao_em_edicao.dificuldade = self.gvar.dificuldade.get()
    #     self.gvar.questao_em_edicao.peso = self.gvar.peso.get()
    #     self.gvar.questao_em_edicao.pergunta = self.gvar.pergunta.get_texto_completo()
    #     self.gvar.questao_em_edicao.alternativas = self.get_opcoes()
    #
    #     self.gvar.quadro_de_questoes.salvar_edicao_de_questao()
    #
    #     self.gvar.questao_em_edicao = None
    #     self.gvar.reseta_informacoes()

    # def get_opcoes(self) -> list[tuple[str, bool]]:
    #     def seleciona_bt(indice: int) -> [CTkRadioButton, CTkCheckBox]:
    #         tipo = self.gvar.tipo.get()
    #         if tipo == ME:
    #             return self.gvar.lista_rd_bts[indice]
    #         elif tipo == MEN or tipo == VF:
    #             return self.gvar.lista_ck_bts[indice]
    #
    #     def verifica_correta(botao: [CTkRadioButton, CTkCheckBox], indice: int) -> bool:
    #         if self.gvar.tipo.get() == ME:
    #             return self.gvar.opcao_correta_radio_bt.get() == indice
    #         return botao.get()
    #
    #     opcoes = list()
    #     for indice in range(self.gvar.contador_de_opcoes.get()):
    #         txt_box: CaixaDeTexto = self.gvar.lista_txt_box[indice]
    #         texto = txt_box.get_texto_completo()
    #
    #         correta = verifica_correta(seleciona_bt(indice), indice)
    #
    #         opcoes.append((texto, correta))
    #
    #     return opcoes
    #
    # def exportar(self):
    #     if self.gvar.caminho_atual is None:
    #         self.gvar.caminho_atual = self.gvar.arquivos.caminho_para_salvar('Exportar')
    #
    #     self.gvar.arquivos.exportar(self.gvar.caminho_atual, self.gvar.quadro_de_questoes.lista_de_questoes())
    #
    #     self.gvar.exportado = True
    #     showinfo('Exportado', 'O banco de dados foi criado com sucesso!')
