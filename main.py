import re
from os.path import basename
from pathlib import Path
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import showerror, showinfo, showwarning, askyesnocancel, askyesno

from customtkinter import *

from Modules.constants import *
from Modules.arquivos import Arquivos
from Modules.imagens import Imagens
from Modules.perfil import Perfil
from Modules.configuracoes import *
from Modules.quadro_de_questoes.quadro_de_questoes import QuadroDeQuestoes
from Modules.painel_de_configuracoes import PainelDeConfiguracoes
from Modules.corretor_ortografico import CorretorOrtografico
from Modules.models.questao import ModeloQuestao
from Modules.models.caixa_de_texto import CaixaDeTexto
from Modules.atualizacao import Atualizacao


# noinspection PyAttributeOutsideInit
class Main(CTk):
    __version__ = 3.1
    __author__ = 'Edimar Freitas de Sá'
    __annotations__ = 'edimarfreitas95@gmail.com'

    def exportar(self):
        if not self.caminho_arquivo:
            self.caminho_arquivo = self.arquivos.caminho_salvar_para_salvar('Exportar para')

        retorno = self.arquivos.exportar(self.caminho_arquivo, self.questions_board.lista_de_questoes())
        if not retorno:
            showerror('Não foi possível exportar', 'Para exportar é necessário que o arqivo esteja fechado.'
                                                   '\nConfirme que nenhum arquivo xlsx com mesmo nome esteja aberto.')
        self.exportado = True
        showinfo('Exportado', 'O banco de dados foi criado com sucesso!')
        self.reseta_geral()

    def abrir(self):
        if self.contador_de_opcoes:
            resposta = askyesno(
                'Questão em edição',
                'Você tem questões em edição, deseja salva-la antes de abrir um novo arquivo?'
            )
            if resposta:
                self.salvar_como()

        self.reseta_question_board()
        self.exportado = True
        self.reseta_informacoes()

        self.caminho_arquivo = self.arquivos.buscar_arquivo_para_abrir()
        if not self.caminho_arquivo:
            return
        questoes = self.arquivos.carrega_banco_de_dados(self.caminho_arquivo)

        for questao in questoes:
            self.questions_board.adiciona_questao(questao)

        self.set_quantidade_de_questoes()
        self.set_titulo()

    def salvar_como(self):
        self.caminho_arquivo = self.arquivos.caminho_salvar_para_salvar('Salvar como')
        self.exportar()
        self.set_titulo()

    def seleciona_caminho(self, titulo: str):
        self.caminho_arquivo = asksaveasfilename(confirmoverwrite=True, defaultextension=DEFAULT_EXTENSION,
                                                 filetypes=FILETYPES, initialdir=self.local, title=titulo)

    def altera_unidade_padrao(self):
        nova_unidade = self.var_nova_unidade_padrao.get()
        self.unidade.set(nova_unidade)
        self.salva_informacao('perfil', 'unidade_padrao', nova_unidade)

    def altera_alternativa(self, e=None):
        quantidade_de_questoes = self.contador_de_opcoes
        for indice in range(quantidade_de_questoes):
            self.rm_alternativa()
        for indice in range(quantidade_de_questoes):
            self.add_alternativa()
        self.organiza_ordem_tabulacao()

    def set_titulo(self):
        self.title(f'Gerador de questões - {basename(self.caminho_arquivo)}' if self.caminho_arquivo else 'Gerador de questões')

    def set_quantidade_de_questoes(self):
        self.var_quantidade_de_questoes.set(f'Número de questões: '
                                            f'{self.questions_board.quantidade_de_questoes_registradas()}')

    def organiza_ordem_tabulacao(self):
        ordem_widgets = [
            self.codigo_do_curso,
            self.tempo,
            self.peso,
            self.pergunta,
        ]

        for widget in ordem_widgets:
            widget.lift()

    def get_opcao_bt(self, indice) -> [CTkRadioButton, CTkCheckBox]:
        def show_rd_bt() -> CTkRadioButton:
            rd_bt = getattr(self, f'rd_button_opcao{indice}')
            return rd_bt

        def show_ck_bt() -> CTkCheckBox:
            ck_bt = getattr(self, f'ck_button_opcao{indice}')
            return ck_bt

        def show_dissert():
            pass

        tipos_btn = {
            ME: show_rd_bt,
            MEN: show_ck_bt,
            VF: show_ck_bt,
            D: show_dissert
        }
        return tipos_btn[self.get_tipo]()

    def show_opcao(self, indice):
        pos_y = self.calcula_posicao_y(indice) + 0.04
        pos_x = 0.95

        self.get_opcao_bt(indice).place(relx=pos_x, rely=pos_y)

    def editar_questao(self, questao: ModeloQuestao):
        self.reseta_informacoes()
        self.questao_em_edicao = questao
        self.codigo_do_curso.insert(0, questao.codigo)
        self.tempo.insert(0, questao.tempo)
        self.tipo.set(questao.tipo)
        self.dificuldade.set(questao.dificuldade)
        self.peso.insert(0, questao.peso)
        self.pergunta.insert(0.0, questao.pergunta)
        for alternativa, correta in questao.alternativas:
            self.add_alternativa(alternativa)
            if correta:
                opcao_bt = self.get_opcao_bt(self.contador_de_opcoes - 1)
                opcao_bt.select()

    @property
    def get_opcoes(self) -> list[tuple[str, bool]]:
        def verifica_correta(botao, indice):
            if self.get_tipo == ME:
                return self.var_opcao_correta_radio_bt.get() == indice
            return botao.get()

        opcoes = list()
        for indice in range(self.contador_de_opcoes):
            texto: CaixaDeTexto = self.txt_opcao(indice)
            alternativa = texto.get_texto_completo()
            correta = verifica_correta(self.get_opcao_bt(indice), indice)
            opcoes.append((alternativa, correta))
        return opcoes

    @property
    def get_tipo(self):
        return self.tipo.get()

    @property
    def get_unidade(self):
        return self.unidade.get()

    @property
    def get_codigo(self):
        return self.codigo_do_curso.get()

    @property
    def get_tempo(self):
        tempo = self.tempo.get()
        if not tempo:
            tempo = '00:00:00'
        return tempo

    @property
    def get_dificuldade(self):
        return self.dificuldade.get()

    @property
    def get_peso(self):
        peso = self.peso.get()
        if not peso:
            peso = 1
        return peso

    @property
    def get_pergunta(self):
        return self.pergunta.get_texto_completo()

    @staticmethod
    def calcula_posicao_y(multiplo):
        return (0.18 * multiplo) + 0.1

    def reseta_informacoes(self):
        self.unidade.set(self.configuracao_unidade_padrao)
        self.codigo_do_curso.delete(0, 'end')
        self.tempo.delete(0, 'end')
        self.peso.delete(0, 'end')
        self.var_opcao_correta_radio_bt.set(0)

        if self.var_apagar_enunciado:
            self.pergunta.delete(0.0, 'end')

        for indice in range(5):
            self.txt_opcao(indice).delete(0.0, 'end')
            self.rm_alternativa()

        self.pergunta.focus()
        self.set_quantidade_de_questoes()

    def salvar_edicao(self):
        self.questao_em_edicao.campo_unidade = self.get_unidade
        self.questao_em_edicao.codigo = self.get_codigo
        self.questao_em_edicao.tempo = self.get_tempo
        self.questao_em_edicao.tipo = self.get_tipo
        self.questao_em_edicao.dificuldade = self.get_dificuldade
        self.questao_em_edicao.peso = self.get_peso
        self.questao_em_edicao.pergunta = self.get_pergunta
        self.questao_em_edicao.alternativas = self.get_opcoes

        self.questions_board.salvar_edicao_de_questao(self.questao_em_edicao)

        self.questao_em_edicao = None
        self.reseta_informacoes()

    def init_binds(self):
        def ctrl_events(e):
            key = str(e.keysym).lower()

            def seleciona_tipo(indice: int):
                self.tipo.set(self.tipos[indice])
                self.altera_alternativa()

            def seleciona_dificuldade(indice: int):
                self.dificuldade.set(self.dificuldades[indice - 4])

            events = {
                'e': self.exportar,
                's': self.salvar,
                'o': self.abrir,
                'equal': self.add_alternativa,
                'plus': self.add_alternativa,
                'minus': self.rm_alternativa,
                '1': seleciona_tipo,
                '2': seleciona_tipo,
                '3': seleciona_tipo,
                '4': seleciona_dificuldade,
                '5': seleciona_dificuldade,
                '6': seleciona_dificuldade,
            }

            if key in events:
                if key.isdigit():
                    return events[key](int(key))
                else:
                    return events[key]()

        def key_events(e):
            key = e.keysym
            events = {
                'F1': self.abre_atalhos,
                'F4': self.evento_de_fechamento_da_tela,
                'F12': self.salvar_como,
            }
            if key in events.keys():
                return events[key]()

        self.bind('<Control-KeyRelease>', ctrl_events)
        self.bind('<KeyRelease>', key_events)
        self.protocol(self.protocol()[0], self.evento_de_fechamento_da_tela)

    def evento_de_fechamento_da_tela(self):
        if not self.exportado:
            tittle = 'Salvamento pendente'
            information = 'Uma ou mais questões estão em edição e não foram exportadas.\n' \
                          'Deseja exportar as alterações antes de sair?'
            resposta = askyesnocancel(tittle, information)
            if resposta is None:  # Se resposta for cancelar
                return
            elif resposta:  # Se resposta for sim
                self.exportar()
        # Se resposta for não ou se arquivo já estiver sido exportado
        self.quit()

    def abre_atalhos(self):
        self.abre_menu_configuracoes()
        self.painel_de_configuracoes.abre_ajuda()

    def reseta_question_board(self):
        self.questions_board.destroy()
        self.create_questions_frame()

    def reseta_geral(self):
        self.reseta_informacoes()
        self.reseta_question_board()
        self.caminho_arquivo = None
        self.questao_em_edicao = None
        self.set_titulo()
        self.set_quantidade_de_questoes()

    def verifica_digito(self, keysym):
        pass

    def verifica_atualizacao(self):
        if not getattr(self, 'atualizador', False):
            self.atualizador = Atualizacao(self.__version__, self.local)

        resposta = None
        if self.atualizador.atualizacao_disponivel:
            resposta = askyesno(
                'Nova atualização disponível',
                f'O programa está atualmente na versão {self.__version__}.\n'
                f'A versão disponível é a {self.atualizador.versao_recente}.\n'
                f'Deseja atualizar agora?'
            )

        if resposta:
            self.atualizador.atualiza()
            self.after(1200, self.evento_de_fechamento_da_tela)

    def verifica_texto_opcoes(self):
        if self.get_tipo == D:
            return False
        for indice in range(self.contador_de_opcoes):
            opcao: CaixaDeTexto = self.txt_opcao(indice)
            texto = opcao.get_texto_completo()
            if not texto:
                return True
        return False

    def txt_opcao(self, indice):
        return getattr(self, f'txt_opcao{indice}')


if __name__ == '__main__':
    app = Main()
    app.mainloop()
