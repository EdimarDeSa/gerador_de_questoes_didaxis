from tkinter.messagebox import askyesnocancel, showinfo

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
        largura, altura = 1500, 750
        pos_x = (self.winfo_screenwidth() - largura) // 2
        pos_y = (self.winfo_screenheight() - altura) // 2 - 35
        self.geometry(f'{largura}x{altura}+{pos_x}+{pos_y}')
        self.resizable(OFF, OFF)
        self.configure(**self.configs.root_configs)
        self.configura_aparencia()
        self.set_titulo('Editor de questões')

    def configura_aparencia(self):
        set_appearance_mode(self.perfil.aparencia_do_sistema)
        set_default_color_theme(self.perfil.cor_padrao)
        self.altera_escala_do_sistema(self.perfil.escala_do_sistema)

    def configura_variaveis(self):
        self.gvar = VariaveisGlobais(self.arquivos, self.configs, self.perfil, self.imagens)
        self.gvar.corretor_ortografico = CorretorOrtografico(self.perfil)
        self.gvar.exit = self.evento_de_fechamento_da_tela
        self.gvar.atualiza_titulo = self.set_titulo
        self.gvar.cmd_altera_escala_do_sistema = self.altera_escala_do_sistema

    def configura_ui(self):
        JanelaQuantidadeDeQuestoes(self, self.gvar).place(relx=0.01, rely=0.02, relwidth=0.08, relheight=0.19)
        JanelaParametrosDaQuestao(self, self.gvar).place(relx=0.1, relwidth=0.395, rely=0.02, relheight=0.19)
        JanelaEnunciadoDaQuestao(self, self.gvar).place(relx=0.01, rely=0.23, relwidth=0.485, relheight=0.19)
        JanelaOpcoesDaQuestao(self, self.gvar).place(relx=0.01, rely=0.44, relwidth=0.485, relheight=0.46)
        QuadroDeQuestoes(self, self.gvar).place(relx=0.505, rely=0.02, relwidth=0.485, relheight=0.96)
        JanelaDeBotoes(self, self.gvar).place(relx=0.01, rely=0.92, relwidth=0.485, relheight=0.06)

    def altera_escala_do_sistema(self, nova_escala):
        nova_escala_float = int(nova_escala.replace("%", "")) / 100
        set_widget_scaling(nova_escala_float)
        self.perfil.salva_informacao_perfil('escala_do_sistema', nova_escala)

    def set_titulo(self, texto: str = 'Editor de questões'):
        self.title(texto)

    def evento_de_fechamento_da_tela(self):
        if not self.gvar.exportado:
            resposta = askyesnocancel(
                'Salvamento pendente',
                'Uma ou mais questões estão em edição e não foram exportadas.\n'
                'Deseja exportar as alterações antes de sair?'
            )
            if resposta is None:
                return
            elif resposta:
                result = self.gvar.arquivos.exportar(self.gvar.caminho_atual, self.gvar.quadro_de_questoes.lista_de_questoes())
                if not result:
                    return
        self.gvar.corretor_ortografico = None
        showinfo('Exportado', 'O banco de dados foi criado com sucesso!')
        os.kill(os.getpid(), os.CLD_KILLED)


if __name__ == '__main__':
    Main()
