from customtkinter import *

from Modules.arquivos import *
from Modules.imagens import *
from Modules.corretor_ortografico import CorretorOrtografico
from Modules.constants import *
from Modules.configuracoes import *
from Modules.perfil import *
from Modules.janelas import *
from Modules.models.caixa_de_texto import *


# noinspection PyAttributeOutsideInit
class Main(CTk):
    def __init__(self):
        super(Main, self).__init__()

        self.arquivos = Arquivos()
        self.configs = Configuracoes(self.arquivos)
        self.perfil = Perfil(self.arquivos)
        self.imagens = Imagens(self.arquivos)
        self.corretor_ortografico = CorretorOrtografico(self.perfil)

        self.configura_ui_master()
        self.configura_variaveis()

        self.configura_ui_form_questao()
        self.configura_ui_quadro_de_questoes()

        self.mainloop()

    def configura_ui_master(self):
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()
        largura_do_quadro = int(largura_tela * 0.95)
        altura_do_quadro = int(altura_tela * 0.9)
        x_inicial = (largura_tela - largura_do_quadro) // 2
        y_inicial = (altura_tela - altura_do_quadro - 75) // 2

        self.geometry(f'{largura_do_quadro}x{altura_do_quadro}+{x_inicial}+{y_inicial}')
        self.resizable(False, False)
        self.configure(**self.configs.root_configs)

        self.altera_dark_mode(self.perfil.aparencia_do_sistema)
        set_default_color_theme(self.perfil.cor_padrao)
        self.altera_escala_do_sistema(self.perfil.escala_do_sistema)

        self.set_titulo()

    def set_titulo(self, texto: str = 'Editor de questões'):
        self.title(texto)

    def configura_variaveis(self):
        self.var_opcao_correta_radio_bt = IntVar(value=0)
        self.var_quantidade_de_questoes = StringVar(value='Quantidade de questões: - ')
        self.var_contador_de_opcoes = 0

        # Variaveis do perfil do usuario
        self.var_apagar_enunciado = BooleanVar(value=False)
        self.var_dark_mode = StringVar(value='system')
        self.var_escala_do_sistema = StringVar(value='100%')
        self.var_unidade_padrao = StringVar()

        # Variaveis das opcoes
        self.var_lista_txt_box: list[CaixaDeTexto] = []
        self.var_lista_rd_bts: list[CTkRadioButton] = []
        self.var_lista_ck_bts: list[CTkCheckBox] = []

    def configura_ui_form_questao(self):
        self.janela_quantidade_de_questoes = JanelaQuantidadeDeQuestoes(
            self, self.configs, self.var_quantidade_de_questoes
        )
        self.janela_quantidade_de_questoes.place(relx=0.01, rely=0.02, relwidth=0.08, relheight=0.19)

        self.janela_parametros_da_questao = JanelaParametrosDaQuestao(
            self, self.configs, self.var_unidade_padrao
        )
        self.janela_parametros_da_questao.place(relx=0.1, relwidth=0.395, rely=0.02, relheight=0.19)

        self.janela_enunciado_da_questao = JanelaEnunciadoDaQuestao(
            self, self.configs, self.var_contador_de_opcoes, self.janela_parametros_da_questao.tipo,
            self.var_lista_txt_box, self.var_lista_rd_bts, self.var_lista_ck_bts, corretor=self.corretor_ortografico
        )
        self.janela_enunciado_da_questao.place(relx=0.01, rely=0.23, relwidth=0.485, relheight=0.19)

        self.janela_opcoes_da_questao = JanelaOpcoesDaQuestao(
            self, self.configs, self.var_opcao_correta_radio_bt, self.var_lista_txt_box, self.var_lista_rd_bts,
            self.var_lista_ck_bts, corretor=self.corretor_ortografico
        )
        self.janela_opcoes_da_questao.place(relx=0.01, rely=0.44, relwidth=0.485, relheight=0.46)

        self.janela_de_botoes = JanelaDeBotoes(
            self, self.configs, self.imagens, self.arquivos, self.perfil,
            self.var_unidade_padrao, self.var_apagar_enunciado, self.var_dark_mode, self.var_escala_do_sistema
        )
        self.janela_de_botoes.place(relx=0.01, rely=0.92, relwidth=0.485, relheight=0.06)

    def configura_ui_quadro_de_questoes(self):
        pass

    def altera_escala_do_sistema(self, nova_escala):
        nova_escala_float = int(nova_escala.replace("%", "")) / 100
        set_widget_scaling(nova_escala_float)

    def altera_dark_mode(self, modo: str):
        set_appearance_mode(modo)


if __name__ == '__main__':
    Main()
