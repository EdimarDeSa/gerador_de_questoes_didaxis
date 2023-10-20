from typing import Callable

from customtkinter import CTkFrame, CTk, CTkLabel, CTkButton, END, CTkRadioButton, CTkCheckBox, NSEW

from ..configuration_manager import ConfigurationManager
from ..models.globalvars import VariaveisGlobais
from ..models.caixa_de_texto import CaixaDeTexto
from ..constants import VF, D, ME, MEN


class JanelaEnunciadoDaQuestao(CTkFrame):
    def __init__(self, master: CTk, configuration_manager: ConfigurationManager, variaveis_globais: VariaveisGlobais,
                 **kwargs):
        super().__init__(master, **kwargs)

        self.cnf_manager = configuration_manager
        self.gvar = variaveis_globais
        
        label_configs = self.cnf_manager.label_titulos_configs

        CTkLabel(self, text='Enunciado da questão', **label_configs).place(relx=0.02, rely=0.025, relwidth=0.85)
        pergunta = CaixaDeTexto(self, **self.cnf_manager.text_configs, height=90)
        pergunta.place(relx=0.02, rely=0.25, relwidth=0.85, relheight=0.7)
        self.gvar.corretor_ortografico.monitora_textbox(pergunta)

        CTkLabel(self, text='Opção', **label_configs).place(relx=0.85, rely=0.025, relwidth=0.15)
        CTkButton(self, text='+', width=30, height=30, command=self.gvar.add_alternativa,
                  **self.cnf_manager.buttons_configs).place(relx=0.905, rely=0.35)
        CTkButton(self, text='-', width=30, height=30, command=self.gvar.rm_alternativa,
                  **self.cnf_manager.buttons_configs).place(relx=0.905, rely=0.65)

        # ------ Adiciona variáveis globais ------ #

        self.gvar.pergunta = pergunta
        # self.gvar.editar_questao = self.editar_questao

    # def editar_questao(self, questao: int):
    #     self.gvar.reseta_informacoes()
    #
    #     self.gvar.questao_em_edicao = questao
    #
    #     self.gvar.sub_categoria.insert(0, questao.subcategoria)
    #     self.gvar.tempo.insert(0, questao.tempo)
    #     self.gvar.tipo.set(questao.tipo)
    #     self.gvar.dificuldade.set(questao.dificuldade)
    #     self.gvar.peso.insert(0, questao.peso)
    #     self.gvar.pergunta.insert(0.0, questao.pergunta)
    #
    #     for alternativa, correta in questao.alternativas:
    #         self.gvar.add_alternativa(alternativa)
    #         if correta:
    #             opcao_bt = self._get_opcao_bt(self.gvar.contador_de_opcoes.get() - 1, self.gvar.tipo.get())
    #             opcao_bt.select()
