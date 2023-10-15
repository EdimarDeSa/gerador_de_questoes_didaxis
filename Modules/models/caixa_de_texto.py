from customtkinter import CTkTextbox
from tkinter.messagebox import showwarning

from Modules.constants import *


__all__ = ['CaixaDeTexto']


class CaixaDeTexto(CTkTextbox):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, border_color='red', **kwargs)

        self.bind('<KeyRelease>', self.verifica_quantidade_digitos, add='+')
        self.palavras_com_sugestoes: dict = {}

        self.alerta_exibido = False

    def get_possiveis_correcoes(self, palavra) -> list:
        return self.palavras_com_sugestoes.get(palavra, {}).get('sugestoes', ['Sem sugestões'])

    def registra_possiveis_correcoes(self, palavra: str, novas_correcoes: set):
        if novas_correcoes:
            lista_correcoes = list(novas_correcoes) if len(novas_correcoes) < 4 else list(novas_correcoes)[:5]
            self.palavras_com_sugestoes[palavra] = {'sugestoes': lista_correcoes}

    def get_texto_completo(self) -> str:
        return self.get(1.0, 'end-1c')

    def registra_posicao_inicial(self, palavra, start_index):
        self.palavras_com_sugestoes.setdefault(palavra, {})['posicao_inicial'] = start_index

    def get_posicao_inicial(self, palavra):
        return self.palavras_com_sugestoes.get(palavra, {}).get('posicao_inicial')

    def registra_posicao_final(self, palavra, end_index):
        self.palavras_com_sugestoes.setdefault(palavra, {})['posicao_final'] = end_index

    def get_posicao_final(self, palavra):
        return self.palavras_com_sugestoes.get(palavra, {}).get('posicao_final')

    def cria_tag(self, palavra, comando):
        tag_name = f'corretor_ortografico_{self.get_posicao_inicial(palavra)}'
        self.palavras_com_sugestoes.setdefault(palavra, {})['nome_da_tag'] = tag_name

        self.tag_add(tag_name, self.get_posicao_inicial(palavra), self.get_posicao_final(palavra))
        self.tag_config(tag_name, underline=True, underlinefg=RED)
        self.tag_bind(tag_name, '<3>', lambda event, p=palavra: comando(event, p))

    def get_nome_da_tag(self, palavra) -> str:
        return self.palavras_com_sugestoes.get(palavra, {}).get('nome_da_tag')

    def remove_correcao_pela_tag(self, nome_da_tag):
        self.tag_delete(nome_da_tag)
        for palavra, dados in list(self.palavras_com_sugestoes.items()):
            if dados.get('nome_da_tag') == nome_da_tag:
                self.palavras_com_sugestoes.pop(palavra)

    def verifica_quantidade_digitos(self, _):
        total_digitos = len(self.get(1.0, 'end-1c'))
        if total_digitos > MAXIMO_DE_CARACTERES:
            self.tag_add('tamanho', F'1.{MAXIMO_DE_CARACTERES}', 'end-1c')
            self.tag_config('tamanho', background=RED)
            self.configure(border_width=2)

            if self.alerta_exibido: return None
            showwarning(
                'Quantidade de dígitos ultrapassada',
                'Esse texto ficou muito grande, máximo de caracteres é 255.\n'
                'Após importar o banco para o portal, será necessário editar esse texto!'
            )
            self.alerta_exibido = True
        else:
            self.configure(border_width=0)
            self.alerta_exibido = False
