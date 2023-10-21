from customtkinter import CTkFrame, CTk, CTkLabel, CTkButton


from ..Hints import LabelConfigs, EntryConfigs, ButtonConfigs, AddChoiceHandler, RmChoiceHandler, StartMonitorHandler
from FrontEndFunctions.caixa_de_texto import CaixaDeTexto


class JanelaEnunciadoDaQuestao(CTkFrame):
    def __init__(
            self, master: CTk, label_configs: LabelConfigs, entry_configs: EntryConfigs, button_configs: ButtonConfigs,
            add_choice_handler: AddChoiceHandler, rm_choice_handler: RmChoiceHandler,
            start_monitor_handler: StartMonitorHandler,
            **kwargs
    ):
        super().__init__(master, **kwargs)

        button_configs = button_configs.copy()
        button_configs.update({'width': 30, 'height': 30})

        CTkLabel(self, text='Enunciado da questão', **label_configs).place(relx=0.02, rely=0.025, relwidth=0.85)
        pergunta = CaixaDeTexto(self, **entry_configs, height=90)
        pergunta.place(relx=0.02, rely=0.25, relwidth=0.85, relheight=0.7)
        start_monitor_handler(pergunta)

        CTkLabel(self, text='Opção', **label_configs).place(relx=0.85, rely=0.025, relwidth=0.15)
        CTkButton(self, text='+', command=add_choice_handler, **button_configs).place(relx=0.905, rely=0.35)
        CTkButton(self, text='-', command=rm_choice_handler, **button_configs).place(relx=0.905, rely=0.65)
