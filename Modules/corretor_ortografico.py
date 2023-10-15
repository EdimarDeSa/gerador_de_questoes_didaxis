from threading import Thread
from tkinter import Menu, TclError

from spellchecker import *

from .models.caixa_de_texto import *
from Modules.perfil import *
from Modules.constants import *


__all__ = ['CorretorOrtografico']


class CorretorOrtografico(SpellChecker):
    def __init__(self, perfil: Perfil, timeout=500, max_threads=2):
        self.perfil = perfil
        self.__corretor_ortografico = SpellChecker(
            distance=2, case_sensitive=True, local_dictionary=str(perfil.CAMINHO_DICIONARIO_PESSOAL),
        )

        self.__timeout = timeout
        self.__max_threads = max_threads
        self.__timer = None
        self.__timer = None
        self.__running_threads = 0

    def monitora_textbox(self, textbox: CaixaDeTexto):
        textbox.bind('<KeyRelease>', lambda event: self.__inicia_temporizador(event), add='+')

    def __inicia_temporizador(self, event):
        if len(event.keysym) != 1:
            return
        self.__text_widget: CaixaDeTexto = event.widget.master
        if self.__timer:
            self.__text_widget.after_cancel(self.__timer)
        self.__timer = self.__text_widget.after(self.__timeout, self.__verifica_thread_para_inicio_da_correcao)

    def __verifica_thread_para_inicio_da_correcao(self):
        if self.__running_threads < self.__max_threads:
            self.__running_threads += 1
            Thread(target=self.__inicia_correcao).start()

    def __inicia_correcao(self):
        self.__limpa_correcoes_anteriores()

        palavras = self.__corretor_ortografico.split_words(self.__text_widget.get_texto_completo())
        palavras_erradas = self.__corretor_ortografico.unknown(palavras)
        for palavra in palavras_erradas:
            sugeridas = self.__corretor_ortografico.candidates(palavra)
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

    def __limpa_correcoes_anteriores(self):
        for nome_da_tag in self.__text_widget.tag_names():
            if nome_da_tag.startswith("corretor_ortografico_"):
                self.__text_widget.remove_correcao_pela_tag(nome_da_tag)

    def show_correction_menu(self, event, palavra):
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

    def __aplica_correcao(self, correction, palavra, text_widget):
        start_index = text_widget.get_posicao_inicial(palavra)
        end_index = text_widget.get_posicao_final(palavra)
        tag_name = text_widget.get_nome_da_tag(palavra)

        if correction == ADD:
            self.__aplica_adicao(text_widget, start_index, end_index, tag_name, palavra)
        else:
            self.__aplica_substituicao(text_widget, start_index, end_index, tag_name, correction)

        text_widget.palavras_com_sugestoes.pop(palavra)
        text_widget.focus_set()

    def __aplica_adicao(self, text_widget, start_index, end_index, tag_name, palavra):
        self.dicionario_pessoal.add_palavra(palavra)
        text_widget.tag_remove(tag_name, start_index, end_index)

    def __aplica_substituicao(self, text_widget, start_index, end_index, tag_name, correction):
        text_widget.tag_remove(tag_name, start_index, end_index)
        text_widget.delete(start_index, end_index)
        text_widget.insert(start_index, correction)

    def __nada_a_fazer(self):
        pass

