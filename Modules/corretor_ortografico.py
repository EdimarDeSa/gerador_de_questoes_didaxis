from threading import Thread
from tkinter import Menu

from spellchecker.spellchecker import SpellChecker

from .models.caixa_de_texto import CaixaDeTexto
from .configuracoes import Dicionario
import pandas as pd


class PowerfullSpellChecker(SpellChecker):
    def __init__(self, timeout=500, dicionario_pessoal: Dicionario=None, max_threads=2):
        self.__dicionario_pessoal = dicionario_pessoal
        self.__timeout = timeout
        self.__max_threads = max_threads
        self.__timer = None
        self.__running_threads = 0

        self.__inicia_corretor()

    def __inicia_corretor(self):
        self.__corretor_ortografico = SpellChecker(local_dictionary=self.__dicionario_pessoal.caminho_dicionario_pessoal,
                                                   distance=2, case_sensitive=True)

    def monitora_textbox(self, textbox: CaixaDeTexto):
        textbox.bind('<KeyRelease>', self.__inicia_temporizador)

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
            self.__text_widget.registr_possiveis_correcoes(palavra, sugeridas)
        self.__destaca_palavras()

        self.__running_threads -= 1

    def __destaca_palavras(self):
        for palavra in self.__text_widget.palavras_com_sugestoes.keys():
            start_index = self.__text_widget.search(palavra, '1.0', 'end')
            end_index = self.__text_widget.search(r'\s|[\.,!?:;\)]', start_index, stopindex='end', regexp=True)
            self.__text_widget.registra_posicao_inicial(palavra, start_index)
            self.__text_widget.registra_posicao_final(palavra, end_index)
            self.__text_widget.cria_tag(palavra, self.show_correction_menu)

    def __limpa_correcoes_anteriores(self):
        for nome_da_tag in self.__text_widget.tag_names():
            if nome_da_tag.startswith("corretor_ortografico_"):
                self.__text_widget.remove_correcao_pela_tag(nome_da_tag)

    def show_correction_menu(self, e, palavra):
        self.pop_up_menu = Menu(self.__text_widget, tearoff=False, font='arial 12')
        for correction in self.__text_widget.get_possiveis_correcoes(palavra):
            if correction == 'Sem sugestões':
                self.pop_up_menu.add_command(label=correction, command=self.__nada_a_fazer)
                break
            self.pop_up_menu.add_command(label=correction, command=lambda: self.__aplica_correcao(correction, palavra))
        self.pop_up_menu.add_separator()
        self.pop_up_menu.add_command(label='Adicionar', command=lambda: self.__adicionar_palavra(palavra))

        self.pop_up_menu.tk_popup(x=e.x_root, y=e.y_root, entry=0)

    def __aplica_correcao(self, correction, palavra):
        start_index = self.__text_widget.get_posicao_inicial(palavra)
        end_index = self.__text_widget.get_posicao_final(palavra)
        tag_name = self.__text_widget.get_nome_da_tag(palavra)

        self.__text_widget.delete(start_index, end_index)
        self.__text_widget.tag_remove(tag_name, start_index, end_index)
        self.__text_widget.insert(start_index, correction)
        self.__text_widget.palavras_com_sugestoes.pop(palavra)
        self.__text_widget.focus_set()

    def __nada_a_fazer(self):
        pass

    def __adicionar_palavra(self, palavra):
        self.__dicionario_pessoal.add_palavra(palavra)
        del self.__corretor_ortografico
        self.__inicia_corretor()

