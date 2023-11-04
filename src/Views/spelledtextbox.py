import dataclasses
from tkinter import Event
from tkinter.messagebox import showwarning
from typing import Callable

from customtkinter import CTkTextbox

from src.Constants import MAXIMO_DE_CARACTERES, RED
from src.Contracts.spelledtextbox import SpelledTextBoxContract


@dataclasses.dataclass(frozen=True)
class Vector:
    x: float
    y: float


@dataclasses.dataclass(frozen=True)
class Suggestions:
    vector: Vector
    suggestions: list[str] = dataclasses.field(default_factory=list)


class SpelledTextBox(CTkTextbox, SpelledTextBoxContract):
    def __init__(self, master, input_speller_queue: Callable, **kwargs):
        super().__init__(master, border_color=RED, **kwargs)

        self.bind('<KeyRelease>', self._verifica_quantidade_digitos, add='+')
        self.bind('<KeyRelease>', self._corretor_ortografico, add='+')

        self.palavras_com_suggests: dict = {}
        self.input_speller_queue = input_speller_queue

        self.alerta_exibido = False

    def _corretor_ortografico(self, event: Event):
        if event.keysym.isalpha():
            self.input_speller_queue(self)

    def get_suggestions(self, word: str) -> set[str]:
        return self.palavras_com_suggests.get(word).get('suggests')

    def register_suggestions(self, word: str, suggestions: set[str]) -> None:
        if not suggestions: return

        x = self.search(word, 0.0, nocase=True)
        y = self.index(f"{x} + {len(word)}c")
        vector = Vector(x, y)

        self.get(vector.x, vector.y)

        tag_name = f'{word}_{vector.x}'

        print('register_suggestions')

        suggestions_list = (
            suggestions if len(suggestions) < 4 else list(suggestions)[:5]
        )

        self.tag_add(tag_name, vector.x, vector.y)

        self.tag_config(tag_name, underline=1, foreground='red')

        self.palavras_com_suggests[tag_name] = {Suggestions(
            suggestions=suggestions_list,
            vector=vector
        )}
        print(self.palavras_com_suggests)



    def registra_posicao_inicial(self, palavra, start_index):
        self.palavras_com_suggests.setdefault(palavra, {})[
            'posicao_inicial'
        ] = start_index

    def get_posicao_inicial(self, palavra):
        return self.palavras_com_suggests.get(palavra, {}).get(
            'posicao_inicial'
        )

    def registra_posicao_final(self, palavra, end_index):
        self.palavras_com_suggests.setdefault(palavra, {})[
            'posicao_final'
        ] = end_index

    def get_posicao_final(self, palavra):
        return self.palavras_com_suggests.get(palavra, {}).get(
            'posicao_final'
        )

    def cria_tag(self, palavra, comando) -> None:
        tag_name = f'corretor_ortografico_{self.get_posicao_inicial(palavra)}'
        self.palavras_com_suggests.setdefault(palavra, {})[
            'nome_da_tag'
        ] = tag_name

        self.tag_add(
            tag_name,
            self.get_posicao_inicial(palavra),
            self.get_posicao_final(palavra),
        )
        self.tag_config(tag_name, underline=True, underlinefg=RED)
        self.tag_bind(
            tag_name, '<3>', lambda event, p=palavra: comando(event, p)
        )

    def get_nome_da_tag(self, palavra: str) -> str:
        return self.palavras_com_suggests.get(palavra, {}).get('nome_da_tag')

    def remove_correcao_pela_tag(self, nome_da_tag) -> None:
        self.tag_delete(nome_da_tag)
        for palavra, dados in list(self.palavras_com_suggests.items()):
            if dados.get('nome_da_tag') == nome_da_tag:
                self.palavras_com_suggests.pop(palavra)

    def _verifica_quantidade_digitos(self, _) -> None:
        total_digitos = len(self.get(1.0, 'end-1c'))
        if total_digitos > MAXIMO_DE_CARACTERES:
            self.tag_add('tamanho', f'1.{MAXIMO_DE_CARACTERES}', 'end-1c')
            self.tag_config('tamanho', background=RED)
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
