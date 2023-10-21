from customtkinter import CTk

from FrontEndFunctions import (
    JanelaQuantidadeDeQuestoes,
    JanelaParametrosDaQuestao,
    JanelaEnunciadoDaQuestao,
    JanelaOpcoesDaQuestao,
    # JanelaDeQuestoes,
    # JanelaDeBotoes,
    # JanelaDeConfiguracoes,
)
from back_end import API


class Application:
    def __init__(self, main_window: CTk, api: API):
        self._master = main_window
        self._api = api

        self.configura_ui()
        # self.configura_binds()

        # self.after(500, self.verifica_atualizacao)

        main_window.protocol('WM_DELETE_WINDOW', self._api.evento_de_fechamento_da_tela)

    def configura_ui(self):
        JanelaQuantidadeDeQuestoes(
            self._master, self._api.label_configs, self._api.display_question_count
        ).place(relx=0.01, rely=0.02, relwidth=0.08, relheight=0.19)

        JanelaParametrosDaQuestao(
            self._master, self._api.entry_configs, self._api.label_configs, self._api.list_configs,
            self._api.categoria, self._api.category_list, self._api.sub_categoria, self._api.tempo,
            self._api.type_list, self._api.tipo, self._api.type_change_handler,
            self._api.difficulties_list, self._api.dificuldade, self._api.peso
        ).place(relx=0.1, relwidth=0.395, rely=0.02, relheight=0.19)

        JanelaEnunciadoDaQuestao(
            self._master, self._api.label_configs, self._api.entry_configs, self._api.button_configs,
            self._api.add_choice_handler, self._api.rm_choice_handler, self._api.start_monitor_handler
        ).place(relx=0.01, rely=0.23, relwidth=0.485, relheight=0.19)

        # JanelaOpcoesDaQuestao(
        #     self._master,
        # ).place(relx=0.01, rely=0.44, relwidth=0.485, relheight=0.46)

        # JanelaDeQuestoes(self, self.cnf_manager, self.gvar, self.imagens.bt_editar_questao_img(),
        #                  self.imagens.bt_deletar_questao_img()).place(relx=0.505, rely=0.02, relwidth=0.485,
        #                                                               relheight=0.96)
        #
        # JanelaDeBotoes(self, self.cnf_manager, self.gvar,
        #                self.imagens.bt_configs_img()).place(relx=0.01, rely=0.92, relwidth=0.485, relheight=0.06)
        #
        # JanelaDeConfiguracoes(self, self.cnf_manager, self.gvar)

    def configura_binds(self):
        def ctrl_events(key):
            def seleciona_tipo(indice: str):
                tipos = {'1': ME, '2': MEN, '3': VF}
                self.gvar.tipo.set(tipos.get(indice))
                self.gvar.type_change_handler()

            def seleciona_dificuldade(indice: str) -> None:
                dificuldades = {'4': 'Fácil', '5': 'Médio', '6': 'Difícil'}
                self.gvar.dificuldade.set(dificuldades.get(indice))

            events = {
                # 'e': self.exportar,
                # 's': self.salvar,
                # 'o': abrir,
                'equal': self.gvar.add_choice_handler,
                'plus': self.gvar.add_choice_handler,
                'minus': self.gvar.rm_choice_handler,
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
