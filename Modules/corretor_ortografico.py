from threading import Thread
from pathlib import Path
from tkinter import Menu, TclError, Event
from typing import Callable

from spellchecker import SpellChecker

from .models.caixa_de_texto import CaixaDeTexto
from .constants import *
from Modules.configuration_manager import ConfigurationManager


__all__ = ['CorretorOrtografico']


class CorretorOrtografico:
    def __init__(self, local_dictionary: Path, cmd_add_word: Callable, timeout=500, max_threads=2):
        self.cmd_add_word = cmd_add_word
        self._spell_checker = SpellChecker(distance=2, case_sensitive=True, local_dictionary=str(local_dictionary))

        self.__timeout = timeout
        self.__max_threads = max_threads
        self.__timer = None
        self.__running_threads = 0

    def monitora_textbox(self, textbox: CaixaDeTexto) -> None:
        textbox.bind('<KeyRelease>', self.__inicia_temporizador, add='+')

    def __inicia_temporizador(self, event: Event) -> None:
        if len(event.keysym) != 1:
            return
        self.__text_widget: CaixaDeTexto = event.widget.master
        if self.__timer:
            self.__text_widget.after_cancel(self.__timer)
        self.__timer = self.__text_widget.after(self.__timeout, self.__verifica_thread_para_inicio_da_correcao)

    def __verifica_thread_para_inicio_da_correcao(self) -> None:
        if self.__running_threads < self.__max_threads:
            self.__running_threads += 1
            Thread(target=self.__inicia_correcao).start()

    def __inicia_correcao(self) -> None:
        self.__limpa_correcoes_anteriores()

        palavras = self._spell_checker.split_words(self.__text_widget.get_texto_completo())
        palavras_erradas = self._spell_checker.unknown(palavras)
        for palavra in palavras_erradas:
            sugeridas = self._spell_checker.candidates(palavra)
            self.__text_widget.registra_possiveis_correcoes(palavra, sugeridas)
            try:
                start_index = self.__text_widget.search(palavra, '1.0', 'end')
                end_index = self.__text_widget.search(r'\s|[\.,!?:;\)]', start_index, stopindex='end', regexp=True)
            except TclError:
                return
            self.__text_widget.registra_posicao_inicial(palavra, start_index)
            self.__text_widget.registra_posicao_final(palavra, end_index)
            self.__text_widget.cria_tag(palavra, self.show_correction_menu)

        self.__running_threads -= 1

    def __limpa_correcoes_anteriores(self) -> None:
        for nome_da_tag in self.__text_widget.tag_names():
            if nome_da_tag.startswith("corretor_ortografico_"):
                self.__text_widget.remove_correcao_pela_tag(nome_da_tag)

    def show_correction_menu(self, event, palavra) -> None:
        text_widget: CaixaDeTexto = event.widget.master
        pop_up_menu = Menu(text_widget, tearoff=False, font='arial 12')
        for correction in text_widget.get_possiveis_correcoes(palavra):
            if correction == 'Sem sugestões':
                pop_up_menu.add_command(label=correction, command=self.__nada_a_fazer)
                break
            pop_up_menu.add_command(
                label=correction, command=lambda c=correction, p=palavra, w=text_widget: self.__aplica_correcao(c, p, w)
            )
        pop_up_menu.add_separator()
        pop_up_menu.add_command(
            label=ADD, command=lambda c=ADD, p=palavra, w=text_widget: self.__aplica_correcao(c, p, w)
        )

        pop_up_menu.tk_popup(x=event.x_root, y=event.y_root)

    def __aplica_correcao(self, correction, palavra, text_widget) -> None:
        start_index = text_widget.get_posicao_inicial(palavra)
        end_index = text_widget.get_posicao_final(palavra)
        tag_name = text_widget.get_nome_da_tag(palavra)

        if correction == ADD:
            self.__aplica_adicao(text_widget, start_index, end_index, tag_name, palavra)
        else:
            self.__aplica_substituicao(text_widget, start_index, end_index, tag_name, correction)

        text_widget.palavras_com_sugestoes.pop(palavra)
        text_widget.focus_set()

    def __aplica_adicao(self, text_widget, start_index, end_index, tag_name, palavra) -> None:
        self.cmd_add_word(palavra)
        text_widget.tag_remove(tag_name, start_index, end_index)

    @staticmethod
    def __aplica_substituicao(text_widget, start_index, end_index, tag_name, correction) -> None:
        text_widget.tag_remove(tag_name, start_index, end_index)
        text_widget.delete(start_index, end_index)
        text_widget.insert(start_index, correction)

    @staticmethod
    def __nada_a_fazer() -> None:
        pass
