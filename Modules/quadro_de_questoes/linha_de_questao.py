from tkinter.messagebox import askyesno

from customtkinter import CTkFrame, CTkLabel, CTkButton
from ..models.questao import ModeloQuestao


class LinhaDeQuestao(CTkFrame):
    def __init__(self, master=None, questao=None, eraser_btn_img=None, edit_btn_img=None, **kwargs):
        super(LinhaDeQuestao, self).__init__(master=master, **kwargs)
        self.questao: ModeloQuestao = questao
        self.__eraser_btn_img = eraser_btn_img
        self.__edit_btn_img = edit_btn_img

        self.__configura_colunas()

    def __configura_colunas(self):
        self.__label = CTkLabel(self, text=self.questao.pergunta, width=550, anchor='w', height=30, wraplength=540)
        self.__label.grid(row=0, column=0, pady=5, padx=(5, 0))

        CTkButton(self, text="", width=30, height=30, image=self.__edit_btn_img,
                  command=self.__editar).grid(column=1, row=0, padx=15)

        CTkButton(self, text="", width=30, height=30, image=self.__eraser_btn_img,
                  command=self.__botao_delete).grid(column=2, row=0, padx=15)

    def __botao_delete(self):
        if self.__tem_certeza():
            self.master.delete_event(self)
            self.destroy()

    @staticmethod
    def __tem_certeza() -> bool:
        resposta = askyesno('Deseja deletar a questão?',
                            'Tem certeza que deseja deletar a questão? Esse processo não poderá ser desfeito.')
        return resposta

    def __editar(self):
        self.master.master.master.master.master.editar_questao(self.questao)

    def salva_questao_editada(self, nova_questao: ModeloQuestao):
        del self.questao
        self.questao = nova_questao
        self.__label.configure(text=self.questao.pergunta)