from typing import Callable
from tkinter.messagebox import showinfo, showerror, showwarning, askyesnocancel, askretrycancel

from customtkinter import StringVar, BooleanVar, IntVar, CTkCheckBox, CTkRadioButton, END, NSEW, CTk

from BackEndFunctions import ConfigurationManager
from BackEndFunctions import FileManager
from BackEndFunctions import QuestionsManager
from BackEndFunctions import SpellerManager
from BackEndFunctions.Constants import PLACE_HOLDER_PESO, PLACE_HOLDER_TEMPO, ME, MEN, VF, D
from BackEndFunctions.aparencia import altera_aparencia, altera_escala, altera_cor_padrao

from FrontEndFunctions import CaixaDeTexto


class API:
    def __init__(self, main_window: CTk):
        self._master = main_window

        # Initiate managers
        self._file = FileManager()
        self._cnf = ConfigurationManager(self._file.base_dir, self._file.read_json, self._file.save_json,
                                         self._file.create_personal_dict)
        self._quest = QuestionsManager()
        self._speller = SpellerManager(self._cnf.PERSONAL_DICT_FILE, self._cnf.add_palavra)

        # Variáveis de perfil
        self.var_apagar_enunciado = BooleanVar(value=self._cnf.apagar_enunciado)
        self.var_aparencia_do_sistema = StringVar(value=self._cnf.aparencia_do_sistema)
        self.escala_do_sistema = StringVar(value=self._cnf.escala_do_sistema)
        self.cor_padrao = StringVar(value=self._cnf.cor_padrao)
        self.var_exportar_automaticamente = BooleanVar(value=self._cnf.exportar_automaticamente)

        # Variáveis de controle
        self.contador_de_opcoes: IntVar = IntVar(value=0)
        self.opcao_correta_radio_bt: IntVar = IntVar(value=0)
        self.display_quantidade_de_questoes: IntVar = IntVar(value=0)
        self.exportado: bool = True

        # Funcoes de Controle
        self.exit = None
        self.atualiza_titulo = None

        # Campos da questao
        self.categoria = StringVar(value=self._cnf.unidade_padrao)
        self.sub_categoria = StringVar()
        self.tempo = StringVar(value=PLACE_HOLDER_TEMPO)
        self.tipo = StringVar(value=self._cnf.tipos[1])
        self.dificuldade = StringVar(value=self._cnf.dificuldades[0])
        self.peso = StringVar(value=PLACE_HOLDER_PESO)
        self.pergunta: CaixaDeTexto | None = None
        self.lista_txt_box: list[CaixaDeTexto | None] = list()
        self.lista_rd_bts: list[CTkRadioButton | None] = list()
        self.lista_ck_bts: list[CTkCheckBox | None] = list()

        # Quadro de questões
        # self.quadro_de_questoes = None

        self.configura_aparencia()
        self.set_titulo('Editor de questões')

    def set_titulo(self, texto: str = 'Editor de questões'):
        self._master.title(texto)

    def configura_aparencia(self):
        # noinspection PyTypeChecker
        altera_aparencia(self.var_aparencia_do_sistema.get())
        altera_cor_padrao(self.cor_padrao.get())
        altera_escala(self.escala_do_sistema.get())

    def reseta_informacoes(self):
        # Janela de parâmetros
        self.categoria.set(self._cnf.unidade_padrao)
        self.sub_categoria.set('')
        self.tempo.set(PLACE_HOLDER_TEMPO)
        self.tipo.set(self._cnf.tipos[1])
        self.dificuldade.set(self._cnf.dificuldades[0])
        self.peso.set(PLACE_HOLDER_PESO)

        # Janela de enunciado
        if self.var_apagar_enunciado:
            self.pergunta.delete(0.0, END)

        # Janela de botões
        self.opcao_correta_radio_bt.set(0)
        for bt in self.lista_ck_bts:
            bt.deselect()
        for txt_box in self.lista_txt_box:
            txt_box.delete(0.0, END)
            self.rm_alternativa()

        self.pergunta.focus()

    def add_alternativa(self, texto_alternativa=None, indice=None) -> None:
        if self.contador_de_opcoes.get() == len(self.lista_txt_box) or self.tipo.get() == D:
            return None

        # Ativado pela alteração de tipo de questão
        if indice is None:
            indice = self.contador_de_opcoes.get()

        # Se a linha for zero, seta como 50, do contrário, 10
        pady = (5 if not indice else 10, 0)

        self.lista_txt_box[indice].grid(column=0, row=indice, sticky=NSEW, pady=pady)

        # Ativado pela edição de questão
        if texto_alternativa is not None:
            self.lista_txt_box[indice].insert(1.0, texto_alternativa)

        bt = self._get_opcao_bt(indice, self.tipo.get())
        bt.grid(column=1, row=indice, padx=(10, 0), pady=pady)

        self.contador_de_opcoes.set(self.contador_de_opcoes.get() + 1)

    def rm_alternativa(self, indice=None) -> None:
        # Se for zero signifca que não tem opção exibida e cancela a ação
        if not self.contador_de_opcoes.get():
            return None

        self.contador_de_opcoes.set(self.contador_de_opcoes.get() - 1)

        # Ativado pela edição de questão
        if indice is None:
            indice = self.contador_de_opcoes.get()

        self.lista_txt_box[indice].grid_forget()
        self.lista_ck_bts[indice].grid_forget()
        self.lista_rd_bts[indice].grid_forget()

    def _get_opcao_bt(self, indice: int, tipo: str) -> CTkRadioButton | CTkCheckBox | None:
        bts = {
            ME: self._get_rd_bt,
            MEN: self._get_ck_bt,
            VF: self._get_ck_bt,
        }
        bt: Callable = bts.get(tipo, None)
        if bt is None:
            return bt
        return bt(indice)

    def _get_rd_bt(self, indice: int) -> CTkRadioButton:
        return self.lista_rd_bts[indice]

    def _get_ck_bt(self, indice: int) -> CTkCheckBox:
        return self.lista_ck_bts[indice]

    def altera_tipo_alternativa(self, _=None):
        quantidade_de_opcoes = self.contador_de_opcoes.get()
        for indice in range(quantidade_de_opcoes):
            self.rm_alternativa(indice=indice)
            self.add_alternativa(indice=indice)
        # self.organiza_ordem_tabulacao()

    def delete_question(self, controle: int) -> None:
        if self._quest.remove_question(controle):
            showinfo('Questão deletada', 'A questão foi deletada com sucesso!')

    def editar_questao(self, controle: int) -> None:
        self.reseta_informacoes()
        question_info: dict = self._quest.get_question(controle)
        self.categoria.set(question_info.get('categoria'))
        self.sub_categoria.set(question_info.get('sub_categoria'))
        self.tempo.set(question_info.get('tempo'))
        self.tipo.set(question_info.get('tipo'))
        self.dificuldade.set(question_info.get('dificuldade'))
        self.peso.set(question_info.get('peso'))
        self.pergunta.insert(1.0, question_info.get('pergunta'))

    def exportar(self):
        pass

    def evento_de_fechamento_da_tela(self):
        if not self.exportado:
            resposta = askyesnocancel(
                'Salvamento pendente',
                'Uma ou mais questões estão em edição e não foram exportadas.\n'
                'Deseja exportar as alterações antes de sair?'
            )
            if resposta is None:
                return
            elif resposta:
                self.exportar()
        exit(0)


if __name__ == '__main__':
    root = CTk()
    f = API()
    root.mainloop()
