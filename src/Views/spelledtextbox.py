import dataclasses
import tkinter as tk
from tkinter import Event, Menu
from tkinter.messagebox import showwarning
from typing import Callable, Dict, NamedTuple

from customtkinter import CTkTextbox

from src.Constants import ADD, MAXIMO_DE_CARACTERES, RED
from src.Contracts.spelledtextbox import SpelledTextBoxContract


@dataclasses.dataclass(frozen=True)
class TagSettings:
    name: str
    suggestions: list[str] = dataclasses.field(default_factory=list)
    index1: float = None
    index2: float = None


class SpelledTextBox(CTkTextbox, SpelledTextBoxContract):
    def __init__(
        self,
        master,
        input_speller_queue: Callable,
        cmd_add_new_word: Callable,
        **kwargs,
    ):
        super().__init__(master, border_color=RED, **kwargs)

        self.bind('<KeyRelease>', self._check_max_caracters, add='+')
        self.bind('<KeyRelease>', self._corretor_ortografico, add='+')

        self.palavras_com_suggests: Dict[str, TagSettings] = dict()
        self.input_speller_queue = input_speller_queue
        self.cmd_add_new_word = cmd_add_new_word

        self.alerta_exibido = False

    def _check_max_caracters(self, _) -> None:
        total_digitos = len(self.get(1.0, 'end-1c'))
        if total_digitos > MAXIMO_DE_CARACTERES:
            index1 = self.index(f"@{MAXIMO_DE_CARACTERES},0")
            print(index1)
            self.tag_add('lenght', f'{index1}', 'end-1c')
            self.tag_config('lenght', background=RED[1])
            self.configure(border_width=2)

            if self.alerta_exibido:
                return None

            showwarning(
                'Quantidade de dígitos ultrapassada',
                'Esse texto ficou muito grande, máximo de caracteres é 255.\n'
                'Após importar o banco para o portal, será necessário editar esse texto!',
            )
            self.alerta_exibido = True
        else:
            self.configure(border_width=0)
            self.alerta_exibido = False

    def _corretor_ortografico(self, event: Event):
        if event.keysym.isalpha(): self.input_speller_queue(self)

    def get_suggestions(self, word: str) -> list[str]:
        return self.palavras_com_suggests.get(word).suggestions

    def register_suggestions(self, word: str, suggestions: set[str]) -> None:
        if not suggestions: return

        tag_name = word
        print(tag_name)

        if tag_name in self.palavras_com_suggests: self.remove_tag(tag_name)

        index1 = self.search(word, 0.0, nocase=True)
        index2 = self.index(f"{index1} + {len(word)}c")

        filtered_suggestions = (suggestions if len(suggestions) < 4 else list(suggestions)[:5])

        tag_settings = TagSettings(tag_name, filtered_suggestions, index1, index2)

        self.palavras_com_suggests[word] = tag_settings

        self.register_tag(tag_name)

    def remove_tag(self, tag_name: str) -> None:
        self.tag_delete(tag_name)
        for word, tag_settings in list(self.palavras_com_suggests.items()):
            if tag_settings.name == tag_name:
                self.palavras_com_suggests.pop(word)
                return

    def register_tag(self, word: str) -> None:
        tag_settings = self.palavras_com_suggests.get(word)

        self.tag_add(
            tag_settings.name, tag_settings.index1, tag_settings.index2
        )

        self.tag_config(tag_settings.name, underline=True, underlinefg='red')

        self.tag_bind(
            tag_settings.name,
            '<3>',
            lambda event, w=word: self.show_correction_menu(event, w),
            add='+',
        )

    def show_correction_menu(self, event: Event, word: str) -> None:
        pop_up_menu = Menu(self, tearoff=False, font='Arial 12')
        for correction in self.palavras_com_suggests.get(word).suggestions:
            if correction == 'Sem sugestões':
                pop_up_menu.add_command(label=correction, command=self._nothing_to_do)
                break

            pop_up_menu.add_command(
                label=correction,
                command=lambda c=correction, w=word: self.__apply_correction(
                    c, w
                ),
            )

        pop_up_menu.add_separator()

        pop_up_menu.add_command(
            label=ADD,
            command=lambda c=ADD, w=word: self.__apply_correction(c, w),
        )
        pop_up_menu.post(event.x_root, event.y_root)

    def __apply_correction(self, correction: str, word: str) -> None:
        tag_settings = self.palavras_com_suggests.pop(word)

        self.remove_tag(tag_settings.name)

        if correction == ADD:
            self.cmd_add_new_word(word)
            return

        if word.istitle(): correction.title()

        self.delete(tag_settings.index1, tag_settings.index2)
        self.insert(tag_settings.index1, correction)

        self.focus_set()

    def remove_all_tags(self):
        for tag_settings in list(self.palavras_com_suggests.values()):
            self.remove_tag(tag_settings.name)

    @staticmethod
    def _nothing_to_do() -> None:
        pass
