from tkinter import Event
from tkinter.messagebox import askyesnocancel

from customtkinter import CTk

from Modules.funcoes import altera_aparencia, altera_escala, altera_cor_padrao
from Modules.janelas import *
from Modules.arquivos import Arquivos
from Modules.constants import ME, MEN, VF, D
from Modules.configuration_manager import ConfigurationManager
from Modules.imagens import Imagens
from Modules.corretor_ortografico import CorretorOrtografico
from Modules.models.globalvars import VariaveisGlobais
from Modules.questions_manager import QuestionsManager


# noinspection PyAttributeOutsideInit
class Main(CTk):
    def __init__(self):
        super().__init__()

        self.arquivos = Arquivos()
        self.cnf_manager = ConfigurationManager(self.arquivos)
        self.imagens = Imagens(self.arquivos.base_dir)
        self.questions_manager = QuestionsManager()

        self.configura_ui_master()
        self.configura_variaveis()
        self.configura_ui()
        self.configura_binds()

        # self.after(500, self.verifica_atualizacao)

        self.protocol('WM_DELETE_WINDOW', self.evento_de_fechamento_da_tela)

        self.mainloop()

    def configura_ui_master(self):
        largura, altura = 1500, 750
        pos_x = (self.winfo_screenwidth() - largura) // 2
        pos_y = (self.winfo_screenheight() - altura) // 2 - 35
        self.geometry(f'{largura}x{altura}+{pos_x}+{pos_y}')
        self.resizable(False, False)
        self.set_titulo('Editor de questões')
        self.configura_aparencia()

    def configura_aparencia(self):
        altera_aparencia(self.cnf_manager.aparencia_do_sistema)
        altera_cor_padrao(self.cnf_manager.cor_padrao)
        altera_escala(self.cnf_manager.escala_do_sistema)

    def configura_variaveis(self):
        self.gvar = VariaveisGlobais(self.cnf_manager)

        self.gvar.corretor_ortografico = CorretorOrtografico(self.cnf_manager.PERSONAL_DICT_FILE,
                                                             self.cnf_manager.add_palavra)
        self.gvar.exit = self.evento_de_fechamento_da_tela
        self.gvar.atualiza_titulo = self.set_titulo

    def configura_ui(self):
        JanelaQuantidadeDeQuestoes(self, self.cnf_manager, self.gvar).place(relx=0.01, rely=0.02, relwidth=0.08,
                                                                            relheight=0.19)
        JanelaParametrosDaQuestao(self, self.cnf_manager, self.gvar).place(relx=0.1, relwidth=0.395, rely=0.02,
                                                                           relheight=0.19)
        JanelaEnunciadoDaQuestao(self, self.cnf_manager, self.gvar).place(relx=0.01, rely=0.23, relwidth=0.485,
                                                                          relheight=0.19)
        JanelaOpcoesDaQuestao(self, self.cnf_manager, self.gvar).place(relx=0.01, rely=0.44, relwidth=0.485,
                                                                       relheight=0.46)
        # JanelaDeQuestoes(self, self.gvar).place(relx=0.505, rely=0.02, relwidth=0.485, relheight=0.96)
        # JanelaDeBotoes(self, self.gvar).place(relx=0.01, rely=0.92, relwidth=0.485, relheight=0.06)

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
                self.gvar.exportar()
        exit(0)

    def configura_binds(self):
        def ctrl_events(key):
            def seleciona_tipo(indice: str):
                tipos = {'1': ME, '2': MEN, '3': VF}
                self.gvar.tipo.set(tipos.get(indice))
                self.gvar.altera_tipo_alternativa()

            def seleciona_dificuldade(indice: str) -> None:
                dificuldades = {'4': 'Fácil', '5': 'Médio', '6': 'Difícil'}
                self.gvar.dificuldade.set(dificuldades.get(indice))

            events = {
                # 'e': self.exportar,
                # 's': self.salvar,
                # 'o': abrir,
                'equal': self.gvar.add_alternativa,
                'plus': self.gvar.add_alternativa,
                'minus': self.gvar.rm_alternativa,
                # 'backspace': self.limpa_tab
                '1': seleciona_tipo,
                '2': seleciona_tipo,
                '3': seleciona_tipo,
                '4': seleciona_dificuldade,
                '5': seleciona_dificuldade,
                '6': seleciona_dificuldade,
            }

            if key in events.keys():
                if key.isdigit():
                    events.get(key)(key)
                else:
                    events.get(key)()

        def key_events(key):
            events = {
                # 'f1': self.abre_atalhos,
                # 'f12': self.gvar.arquivos.salvar_como,
            }
            if key in events.keys():
                return events.get(key)()

        self.bind('<Control-Key>', lambda e: ctrl_events(e.keysym.lower()))
        self.bind('<KeyRelease>', lambda e: key_events(e.keysym.lower()))
