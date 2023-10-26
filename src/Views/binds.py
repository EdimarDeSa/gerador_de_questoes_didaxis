from tkinter import Event

from customtkinter import CTk

from src.Constants import ME, MEN, VF, EASY, MEDIUM, HARD
from src.contracts import ViewsContracts


class Binds:
    def __init__(self, master: CTk, view: ViewsContracts) -> None:
        master.bind('<Control-Key>', self.ctrl_events)
        master.bind('<KeyRelease>', self.key_events)
        
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
            '1': self.seleciona_tipo(key),
            '2': self.seleciona_tipo(key),
            '3': self.seleciona_tipo(key),
            '4': self.seleciona_dificuldade(key),
            '5': self.seleciona_dificuldade(key),
            '6': self.seleciona_dificuldade(key),
        }

        if key in events.keys():
            if key.isdigit():
                events.get(key)(key)
            else:
                events.get(key)()

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
        self.view.type_change(None)

    def seleciona_dificuldade(self, indice: str) -> None:
        dificuldades = {'4': EASY, '5': MEDIUM, '6': HARD}
        self.view.difficulty.set(dificuldades.get(indice))