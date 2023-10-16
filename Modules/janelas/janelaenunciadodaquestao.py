from Modules.models.globalvars import *


class JanelaEnunciadoDaQuestao(CTkFrame):
    def __init__(self, master: CTk, variaveis_globais: VariaveisGlobais, **kwargs):
        super().__init__(master, **kwargs)

        self.gvar = variaveis_globais

        CTkLabel(
            self, text='Enunciado da questão', **self.gvar.configs.label_titulos_configs
        ).grid(row=0, column=0, padx=20)
        self.pergunta = CaixaDeTexto(self, **self.gvar.configs.text_configs, height=90)
        self.pergunta.grid(row=1, column=0, rowspan=2, padx=10, pady=10, ipadx=260)
        self.gvar.corretor_ortografico.monitora_textbox(self.pergunta)

        CTkLabel(self, text='Opção', **self.gvar.configs.label_titulos_configs).grid(row=0, column=1)

        CTkButton(
            self, text='+', width=30, height=30, command=self.add_alternativa,
            **self.gvar.configs.buttons_configs
        ).grid(row=1, column=1, padx=10)

        CTkButton(
            self, text='-', width=30, height=30, command=self.rm_alternativa, **self.gvar.configs.buttons_configs
        ).grid(row=2, column=1, padx=10)

        self.gvar.campo_tipo.configure(command=self._altera_tipo_alternativa)

        # ------ Adiciona variáveis globais ------ #

        self.gvar.campo_pergunta = self.pergunta
        self.gvar.cmd_add_alternativa = self.add_alternativa
        self.gvar.cmd_rm_alternativa = self.rm_alternativa
        self.gvar.cmd_reseta_informacoes = self.reseta_informacoes
        self.gvar.cmd_editar_questao = self.editar_questao

    def add_alternativa(self, texto_alternativa=None, indice=None):
        if self.gvar.contador_de_opcoes.get() == 10 or self.gvar.campo_tipo.get() == D: return None

        if indice is None: indice = self.gvar.contador_de_opcoes.get()

        pady = (50 if not indice else 10, 0)

        texto = self.gvar.lista_txt_box[indice]
        texto.grid(column=0, row=indice, sticky=NSEW, pady=pady)

        if texto_alternativa is not None:
            texto.insert(1.0, texto_alternativa)

        bt = self._get_opcao_bt(indice, self.gvar.campo_tipo.get())
        bt.grid(column=1, row=indice, padx=(10, 0), pady=pady)

        self.gvar.contador_de_opcoes.set(self.gvar.contador_de_opcoes.get() + 1)

    def rm_alternativa(self, indice=None):
        if not self.gvar.contador_de_opcoes.get(): return None

        self.gvar.contador_de_opcoes.set(self.gvar.contador_de_opcoes.get() - 1)

        if indice is None: indice = self.gvar.contador_de_opcoes.get()

        texto: CaixaDeTexto = self.gvar.lista_txt_box[indice]
        texto.grid_forget()

        self.gvar.lista_ck_bts[indice].grid_forget()
        self.gvar.lista_rd_bts[indice].grid_forget()

    def reseta_informacoes(self):
        self.gvar.campo_codigo_do_curso.delete(0, END)
        self.gvar.campo_tempo.delete(0, END)
        self.gvar.campo_peso.delete(0, END)
        self.gvar.opcao_correta_radio_bt.set(0)

        for bt in self.gvar.lista_ck_bts:
            bt.deselect()

        if self.gvar.var_apagar_enunciado: self.gvar.campo_pergunta.delete(0.0, END)

        for txt_box in self.gvar.lista_txt_box:
            txt_box.delete(0.0, END)
            self.gvar.cmd_rm_alternativa()

        self.pergunta.focus()

    def _altera_tipo_alternativa(self, _):
        quantidade_de_opcoes = self.gvar.contador_de_opcoes.get()
        for indice in range(quantidade_de_opcoes):
            self.gvar.cmd_rm_alternativa(indice=indice)
            self.gvar.cmd_add_alternativa(indice=indice)
        # self.organiza_ordem_tabulacao()

    def _get_opcao_bt(self, indice: int, tipo: str) -> [CTkRadioButton, CTkCheckBox]:
        if tipo == ME:
            return self._get_rd_bt(indice)
        elif tipo == MEN or tipo == VF:
            return self._get_ck_bt(indice)
        else:
            return None

    def _get_rd_bt(self, indice) -> CTkRadioButton:
        return self.gvar.lista_rd_bts[indice]

    def _get_ck_bt(self, indice) -> CTkCheckBox:
        return self.gvar.lista_ck_bts[indice]

    def editar_questao(self, questao: ModeloQuestao):
        self.gvar.cmd_reseta_informacoes()

        self.gvar.questao_em_edicao = questao

        self.gvar.campo_codigo_do_curso.insert(0, questao.codigo)
        self.gvar.campo_tempo.insert(0, questao.tempo)
        self.gvar.campo_tipo.set(questao.tipo)
        self.gvar.campo_dificuldade.set(questao.dificuldade)
        self.gvar.campo_peso.insert(0, questao.peso)
        self.gvar.campo_pergunta.insert(0.0, questao.pergunta)

        for alternativa, correta in questao.alternativas:
            self.gvar.cmd_add_alternativa(alternativa)
            if correta:
                opcao_bt = self._get_opcao_bt(self.gvar.contador_de_opcoes.get() - 1, self.gvar.campo_tipo.get())
                opcao_bt.select()
