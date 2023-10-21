from tkinter.messagebox import askyesnocancel

from customtkinter import CTk

from FrontEndFunctions import altera_aparencia, altera_escala, altera_cor_padrao
from back_end import API


class Application:
    def __init__(self, main_window: CTk, api: API):
        self._master = main_window
        self._api = api

        self._configura_ui_master(main_window)
        self.configura_variaveis()
        self.configura_ui()
        self.configura_binds()

        # self.after(500, self.verifica_atualizacao)

        self.protocol('WM_DELETE_WINDOW', self.evento_de_fechamento_da_tela)

        # for i in range(10):
        #     controle = self.quest_manager.create_new_question(
        #         tipo=ME,
        #         peso=self.gvar.peso.get(),
        #         tempo=self.gvar.tempo.get(),
        #         pergunta=f'Pergunta {i}',
        #         categoria=self.gvar.categoria.get(),
        #         subcategoria=self.gvar.sub_categoria.get(),
        #         alternativas=[('Op 1', True), ('Op 2', False), ('Op 3', False), ('Op 4', False), ('Op 5', False)],
        #         dificuldade=self.gvar.dificuldade.get(),
        #     )
        #     self.gvar.quadro_de_questoes.create_new_question_line(f'Pergunta {i}', controle)
        #
        # from Modules.Errors import QuestionMatchError
        # try:
        #     controle = self.quest_manager.create_new_question(
        #         tipo=ME,
        #         peso=self.gvar.peso.get(),
        #         tempo=self.gvar.tempo.get(),
        #         pergunta='Pergunta 1',
        #         categoria=self.gvar.categoria.get(),
        #         subcategoria=self.gvar.sub_categoria.get(),
        #         alternativas=[('Op 1', True), ('Op 2', False), ('Op 3', False), ('Op 4', False), ('Op 5', False)],
        #         dificuldade=self.gvar.dificuldade.get(),
        #     )
        #     self.gvar.quadro_de_questoes.create_new_question_line('Pergunta 1', controle)
        # except QuestionMatchError as e:
        #     print(e)

    def _configura_ui_master(self, main_window: CTk) -> None:
        largura, altura = 1500, 750
        pos_x = (main_window.winfo_screenwidth() - largura) // 2
        pos_y = (main_window.winfo_screenheight() - altura) // 2 - 35
        main_window.geometry(f'{largura}x{altura}+{pos_x}+{pos_y}')
        main_window.resizable(False, False)
        self.set_titulo('Editor de questões')
        self.configura_aparencia()

    def configura_aparencia(self):
        altera_aparencia(self._api.var_aparencia_do_sistema.get())
        altera_cor_padrao(self._api.cor_padrao.get())
        altera_escala(self._api.escala_do_sistema.get())

    def configura_variaveis(self):
        self.gvar = VariaveisGlobais(self.cnf_manager, self.quest_manager)

        self.gvar.corretor_ortografico = SpellerMenager(self.cnf_manager.PERSONAL_DICT_FILE,
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

        JanelaDeQuestoes(self, self.cnf_manager, self.gvar, self.imagens.bt_editar_questao_img(),
                         self.imagens.bt_deletar_questao_img()).place(relx=0.505, rely=0.02, relwidth=0.485,
                                                                      relheight=0.96)

        JanelaDeBotoes(self, self.cnf_manager, self.gvar,
                       self.imagens.bt_configs_img()).place(relx=0.01, rely=0.92, relwidth=0.485, relheight=0.06)

        JanelaDeConfiguracoes(self, self.cnf_manager, self.gvar)

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
