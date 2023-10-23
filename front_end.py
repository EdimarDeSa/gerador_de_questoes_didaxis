from tkinter import Event

from customtkinter import CTk, CTkFrame

from FrontEndFunctions import *
from back_end import API, ME, MEN, VF


class Application:
    def __init__(self, main_window: CTk, api: API):
        self._master = main_window
        self._api = api

        self._set_ui()
        self.configura_binds()

        # self.after(500, self.verifica_atualizacao)

        main_window.protocol('WM_DELETE_WINDOW', self._api.master_wnidow_close_event)

    def _set_ui(self):
        QuestionCountFrame(
            self._master, self._api.label_configs, self._api.display_question_count
        ).place(relx=0.01, rely=0.02, relwidth=0.08, relheight=0.19)

        QuestionParametersFrame(
            self._master, self._api.entry_configs, self._api.label_configs,
            self._api.list_configs, self._api.categoria, self._api.category_list,
            self._api.subcategoria, self._api.tempo, self._api.type_list,
            self._api.tipo, self._api.type_change_handler, self._api.difficulties_list,
            self._api.dificuldade, self._api.peso
        ).place(relx=0.1, relwidth=0.395, rely=0.02, relheight=0.19)

        question_statement_frame = QuestionStatementFrame(
            self._master, self._api.label_configs, self._api.entry_configs,
            self._api.button_configs, self._api.add_choice_handler,
            self._api.rm_choice_handler, self._api.start_monitor_handler
        )
        question_statement_frame.place(relx=0.01, rely=0.23, relwidth=0.485, relheight=0.19)
        self._api.pergunta = question_statement_frame.pergunta

        QuestionChoicesFrame(
            self._master, self._api.label_configs, self._api.text_configs,
            self._api.var_rd_button_value, self._api.start_monitor_handler,
            self._api.lista_txt_box, self._api.lista_rd_bts,
            self._api.lista_ck_bts
        ).place(relx=0.01, rely=0.44, relwidth=0.485, relheight=0.46)

        self._api.questions_frame = QuestionsFrame(
            self._master, self._api.label_configs, self._api.img_edit,
            self._api.img_delete
        )
        self._api.questions_frame.place(relx=0.505, rely=0.02, relwidth=0.485, relheight=0.96)

        CommandButtonsFrame(
            self._master, self._api.img_config, self._api.button_configs,
            self._api.setup_window_handler, self._api.export_handler,
            self._api.save_question_handler,
        ).place(relx=0.01, rely=0.92, relwidth=0.485, relheight=0.06)

        self._api.setuptoplevel = SetupTopLevel(self._master, self._api)

    def configura_binds(self):
        def ctrl_events(event: Event):
            key = event.keysym

            def seleciona_tipo(indice: str):
                tipos = {'1': ME, '2': MEN, '3': VF}
                self._api.tipo.set(tipos.get(indice))
                self._api.type_change_handler()

            def seleciona_dificuldade(indice: str) -> None:
                dificuldades = {'4': 'Fácil', '5': 'Médio', '6': 'Difícil'}
                self._api.dificuldade.set(dificuldades.get(indice))

            events = {
                'e': self._api.export_handler,
                's': self._api.save_question_handler,
                'o': self._api.open_db_handler,
                'equal': self._api.add_choice_handler,
                'plus': self._api.add_choice_handler,
                'minus': self._api.rm_choice_handler,
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
                'f1': self._api.open_help_tab,
                # 'f12': self.gvar.arquivos.salvar_como,
            }
            if key in events.keys():
                return events.get(key)()

        self._master.bind('<Control-Key>', ctrl_events)
        self._master.bind('<KeyRelease>', key_events)
