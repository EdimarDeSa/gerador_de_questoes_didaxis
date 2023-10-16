from tkinter.messagebox import askyesnocancel

from Modules.janelas import *
from Modules.models.globalvars import *
from Modules.quadro_de_questoes.quadro_de_questoes import QuadroDeQuestoes


# noinspection PyAttributeOutsideInit
class Main(CTk):
    def __init__(self):
        super().__init__()

        self.arquivos = Arquivos()
        self.configs = Configuracoes(self.arquivos)
        self.perfil = Perfil(self.arquivos)
        self.imagens = Imagens(self.arquivos)

        self.configura_ui_master()
        self.configura_variaveis()

        self.configura_ui()

        # self.after(500, self.verifica_atualizacao)

        self.mainloop()

    def configura_ui_master(self):
        largura, altura = 1500, 780
        pos_x = (self.winfo_screenwidth() - largura) // 2
        pos_y = (self.winfo_screenheight() - altura - 75) // 2

        self.geometry(f'{largura}x{altura}+{pos_x}+{pos_y}')
        self.resizable(OFF, OFF)
        self.configure(**self.configs.root_configs)

        set_appearance_mode(self.perfil.aparencia_do_sistema)
        set_default_color_theme(self.perfil.cor_padrao)
        self.altera_escala_do_sistema(self.perfil.escala_do_sistema)

        self.set_titulo()

    def configura_variaveis(self):
        self.gvar = VariaveisGlobais(self.arquivos, self.configs, self.perfil, self.imagens)

        # Variáveis de perfil
        self.gvar.var_unidade_padrao = StringVar(value=self.perfil.unidade_padrao)
        self.gvar.var_apagar_enunciado = BooleanVar(value=False)
        self.gvar.var_dark_mode = StringVar(value=APARENCIAS_DO_SISTEMA[2])
        self.gvar.altera_escala_do_sistema = self.altera_escala_do_sistema

        # Variáveis de controle
        self.gvar.contador_de_opcoes = IntVar(value=0)
        self.gvar.opcao_correta_radio_bt = IntVar(value=0)
        self.gvar.display_quantidade_de_questoes = IntVar(value=0)
        self.gvar.exportado = BooleanVar(value=False)
        self.gvar.cmd_exit = self.evento_de_fechamento_da_tela

        # Funcoes de Controle
        self.gvar.corretor_ortografico = CorretorOrtografico(self.perfil)

        # Campos da questao
        self.gvar.lista_txt_box = list()
        self.gvar.lista_rd_bts = list()
        self.gvar.lista_ck_bts = list()

    def configura_ui(self):
        self.janela_quantidade_de_questoes = JanelaQuantidadeDeQuestoes(self, self.gvar)
        self.janela_quantidade_de_questoes.place(relx=0.01, rely=0.02, relwidth=0.08, relheight=0.19)

        self.janela_parametros_da_questao = JanelaParametrosDaQuestao(self, self.gvar)
        self.janela_parametros_da_questao.place(relx=0.1, relwidth=0.395, rely=0.02, relheight=0.19)

        self.janela_enunciado_da_questao = JanelaEnunciadoDaQuestao(self, self.gvar)
        self.janela_enunciado_da_questao.place(relx=0.01, rely=0.23, relwidth=0.485, relheight=0.19)

        self.janela_opcoes_da_questao = JanelaOpcoesDaQuestao(self, self.gvar)
        self.janela_opcoes_da_questao.place(relx=0.01, rely=0.44, relwidth=0.485, relheight=0.46)

        self.quadro_de_questoes = QuadroDeQuestoes(self, self.gvar)
        self.quadro_de_questoes.place(relx=0.505, rely=0.02, relwidth=0.485, relheight=0.96)

        self.janela_de_botoes = JanelaDeBotoes(self, self.gvar)
        self.janela_de_botoes.place(relx=0.01, rely=0.92, relwidth=0.485, relheight=0.06)

    def altera_escala_do_sistema(self, nova_escala):
        nova_escala_float = int(nova_escala.replace("%", "")) / 100
        set_widget_scaling(nova_escala_float)
        self.perfil.salva_informacao_perfil('escala_do_sistema', nova_escala)

    def set_titulo(self, texto: str = 'Editor de questões'):
        self.title(texto)

    def evento_de_fechamento_da_tela(self):
        if not self.gvar.exportado.get():
            tittle = 'Salvamento pendente'
            information = 'Uma ou mais questões estão em edição e não foram exportadas.\n' \
                          'Deseja exportar as alterações antes de sair?'
            resposta = askyesnocancel(tittle, information)
            if resposta is None:  # Se resposta for cancelar
                return
            elif resposta:  # Se resposta for sim
                self.janela_de_botoes.exportar()
        # Se resposta for não ou se arquivo já tiver sido exportado
        sys.exit(0)


if __name__ == '__main__':
    Main()
