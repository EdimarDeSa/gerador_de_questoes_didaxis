from tkinter import Event

from customtkinter import CTk

from src.Constants import EASY, HARD, ME, MEDIUM, MEN, VF
from src.Contracts.viewcontract import ViewContract


# TODO: Cabe melhorias
class Binds:
    def __init__(self, master: CTk, view: ViewContract) -> None:
        master.bind_all('<Control-Key>', self.ctrl_events, add='+')
        master.bind_all('<KeyRelease>', self.key_events, add='+')

        self.view = view

    def ctrl_events(self, event: Event) -> None:
        key = event.keysym

        events = {
            'e': self.view.export_db,
            's': self.view.create_question,
            'o': self.view.open_db,
            'equal': self.view.add_choice,
            'plus': self.view.add_choice,
            'minus': self.view.rm_choice,
            # 'backspace': self.limpa_tab
            '1': self.seleciona_tipo,
            '2': self.seleciona_tipo,
            '3': self.seleciona_tipo,
            '4': self.seleciona_dificuldade,
            '5': self.seleciona_dificuldade,
            '6': self.seleciona_dificuldade,
        }

        if key in events.keys():
            command = events.get(key)

            if key.isdigit():
                command(str(key))
            else:
                command()

    def key_events(self, event: Event) -> None:
        key = event.keysym

        events = {
            'F1': self.view.setuptoplevel.open_help_tab,
            'f12': self.view.export_db,
        }
        if key in events.keys():
            return events.get(key)()

    def seleciona_tipo(self, indice: str) -> None:
        tipos = {'1': ME, '2': MEN, '3': VF}
        self.view.question_type.set(tipos.get(indice))
        self.view.type_change()

    def seleciona_dificuldade(self, indice: str) -> None:
        dificuldades = {'4': EASY, '5': MEDIUM, '6': HARD}
        self.view.difficulty.set(dificuldades.get(indice))
