from Modules.models.globalvars import *
from Modules.painel_de_configuracoes import PainelDeConfiguracoes


class JanelaDeBotoes(CTkFrame):
    def __init__(self, master: CTk, variaveis_globais: VariaveisGlobais, **kwargs):
        super().__init__(master, **kwargs)

        self.gvar = variaveis_globais

        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=3)

        # noinspection PyTypeChecker
        CTkButton(
            self, text=None, width=32, height=32, image=self.gvar.imagens.bt_configs_img(),
            command=self.abre_menu_configuracoes, **self.gvar.configs.buttons_configs
        ).grid(column=0, row=0, pady=10, padx=5)

        CTkButton(
            self, text='Exportar', height=32, command=self.exportar, **self.gvar.configs.buttons_configs
        ).grid(column=1, row=0, pady=10, sticky=NSEW)

        self.bt_salvar = CTkButton(
            self, text='Salvar', height=32, command=self.salvar_questao, **self.gvar.configs.buttons_configs
        )
        self.bt_salvar.grid(column=2, row=0, pady=10, padx=5, sticky=NSEW)

    def abre_menu_configuracoes(self):
        painel = self.children.get('!paineldeconfiguracoes')
        if painel: return painel.focus_force()

        PainelDeConfiguracoes(self, self.gvar)

    def salvar_questao(self):
        if not self.gvar.campo_pergunta.get_texto_completo() or self.verifica_texto_opcoes():
            return showwarning(
                'Pergunta em branco',
                'Para salvar uma questão é necessário que a pergunta e as alternativas ativas não esteja em '
                'branco.'
            )

        print(self.gvar.questao_em_edicao)

        if self.gvar.questao_em_edicao:
            self.salvar_edicao()
            return

        if self.gvar.quadro_de_questoes.verifica_se_pergunta_ja_existe():
            return showinfo('Pergunta repetida', 'Já existe uma questão com a mesma pergunta')

        questao = ModeloQuestao(
            self.gvar.campo_unidade.get(), self.gvar.campo_codigo_do_curso.get(), self.gvar.campo_tempo.get(),
            self.gvar.campo_tipo.get(), self.gvar.campo_dificuldade.get(), self.gvar.campo_peso.get(),
            self.gvar.campo_pergunta.get_texto_completo(), self.get_opcoes()
        )
        self.gvar.quadro_de_questoes.adiciona_questao(questao)

        self.gvar.cmd_reseta_informacoes()
        self.gvar.exportado.set(False)

    def verifica_texto_opcoes(self):
        if self.gvar.campo_tipo.get() != D:
            if not self.gvar.contador_de_opcoes.get():
                return True
            for indice in range(self.gvar.contador_de_opcoes.get()):
                opcao: CaixaDeTexto = self.gvar.lista_txt_box[indice]
                if not opcao.get_texto_completo():
                    return True
        return False

    def salvar_edicao(self):
        self.gvar.questao_em_edicao.unidade = self.gvar.campo_unidade.get()
        self.gvar.questao_em_edicao.codigo = self.gvar.campo_codigo_do_curso.get()
        self.gvar.questao_em_edicao.tempo = self.gvar.campo_tempo.get()
        self.gvar.questao_em_edicao.tipo = self.gvar.campo_tipo.get()
        self.gvar.questao_em_edicao.dificuldade = self.gvar.campo_dificuldade.get()
        self.gvar.questao_em_edicao.peso = self.gvar.campo_peso.get()
        self.gvar.questao_em_edicao.pergunta = self.gvar.campo_pergunta.get_texto_completo()
        self.gvar.questao_em_edicao.alternativas = self.get_opcoes()

        self.gvar.quadro_de_questoes.salvar_edicao_de_questao()

        self.gvar.questao_em_edicao = None
        self.gvar.cmd_reseta_informacoes()

    def get_opcoes(self) -> list[tuple[str, bool]]:
        def seleciona_bt(indice: int) -> [CTkRadioButton, CTkCheckBox]:
            tipo = self.gvar.campo_tipo.get()
            if tipo == ME:
                return self.gvar.lista_rd_bts[indice]
            elif tipo == MEN or tipo == VF:
                return self.gvar.lista_ck_bts[indice]

        def verifica_correta(botao: [CTkRadioButton, CTkCheckBox], indice: int) -> bool:
            if self.gvar.campo_tipo.get() == ME:
                return self.gvar.opcao_correta_radio_bt.get() == indice
            return botao.get()

        opcoes = list()
        for indice in range(self.gvar.contador_de_opcoes.get()):
            txt_box: CaixaDeTexto = self.gvar.lista_txt_box[indice]
            texto = txt_box.get_texto_completo()

            correta = verifica_correta(seleciona_bt(indice), indice)

            opcoes.append((texto, correta))

        return opcoes

    def exportar(self):
        if self.gvar.arquivos.caminho_atual is None:
            self.gvar.arquivos.caminho_atual = self.gvar.arquivos.caminho_para_salvar('Exportar para')

        retorno = self.arquivos(self.caminho_arquivo, self.questions_board.lista_de_questoes())
        if not retorno:
            showerror('Não foi possível exportar', 'Para exportar é necessário que o arqivo esteja fechado.'
                                                   '\nConfirme que nenhum arquivo xlsx com mesmo nome esteja aberto.')
        self.exportado = True
        showinfo('Exportado', 'O banco de dados foi criado com sucesso!')
        self.reseta_geral()
