
from customtkinter import CTkFrame, CTkLabel, CTkScrollableFrame

from ..models.questao import ModeloQuestao
from .linha_de_questao import LinhaDeQuestao


class QuadroDeQuestoes(CTkScrollableFrame):
    def __init__(self, master=None, acesso_imagen=None, **kwargs):
        self.__row_list: list[LinhaDeQuestao] = []
        self.__imagens = acesso_imagen
        self.__zebrar: bool = False
        self.__linha_atual: int = 0
        self.__carrega_imagens()

        super(QuadroDeQuestoes, self).__init__(master=master, **kwargs)
        self.__init_header()

        self.pack(fill='both', expand=True)

    def __init_header(self):
        linha = self.__linha_atual
        cor = self.__select_color()
        cabecalho = CTkFrame(self, fg_color=cor, width=680, height=30)
        cabecalho.grid(row=linha, column=0, columnspan=3, pady=2)

        CTkLabel(cabecalho, text='Enunciado', width=550).grid(row=linha, column=0, pady=2, padx=(2, 0))
        CTkLabel(cabecalho, text='Editar', width=30).grid(row=linha, column=1, padx=15)
        CTkLabel(cabecalho, text='Deletar', width=30).grid(row=linha, column=2, padx=15)
        self.__add_linha()

    def adiciona_questao(self, questao: ModeloQuestao):
        cor = self.__select_color()
        linha = self.__linha_atual

        nw_question_frame = LinhaDeQuestao(self, width=680, height=30, questao=questao,
                                           eraser_btn_img=self.__eraser_img, edit_btn_img=self.__edit_img)
        nw_question_frame.grid(row=linha, column=0, columnspan=3, pady=2)
        nw_question_frame.configure(fg_color=cor)

        self.__row_list.append(nw_question_frame)
        self.__add_linha()

    def __select_color(self) -> str:
        cor = 'green'
        if self.__zebrar:
            cor = 'transparent'
        self.__zebrar = not self.__zebrar
        return cor

    def __reorder_colors(self):
        self.__zebrar = True
        for row in self.__row_list:
            if row.winfo_exists():
                cor = self.__select_color()
                row.configure(fg_color=cor)

    def __add_linha(self):
        self.__linha_atual += 1

    def delete_event(self, row: LinhaDeQuestao):
        self.__row_list.remove(row)
        del row
        self.__reorder_colors()

    def __carrega_imagens(self):
        self.__eraser_img = self.__imagens.bt_deletar_questao_img()
        self.__edit_img = self.__imagens.bt_editar_questao_img()

    def lista_de_questoes(self) -> list[ModeloQuestao]:
        lista = [row.questao for row in self.__row_list]
        return lista

    def editar_questao(self, questao: ModeloQuestao):
        for row in self.__row_list:
            if row.questao == questao:
                row.salva_questao_editada(questao)

    def verifica_se_pergunta_ja_existe(self, pergunta: str) -> bool:
        perguntas = []
        if self.__row_list:
            perguntas = [questao.pergunta for questao in self.lista_de_questoes()]
        return pergunta in perguntas

    def quantidade_de_questoes_registradas(self) -> int:
        total = len(self.__row_list)
        return total
