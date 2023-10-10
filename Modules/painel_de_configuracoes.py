from subprocess import call

from customtkinter import *

from Modules. constants import *


class PainelDeConfiguracoes(CTkToplevel):
    def __init__(self, master=None, **kwargs):
        self.__master = master
        super(PainelDeConfiguracoes, self).__init__(master, **kwargs)
        self.configura_tela()

        self.__init_tabela()
        self.focus()

    def configura_tela(self):
        self.geometry('700x500')
        self.resizable(False, False)

    def __init_tabela(self):
        self.tabview = CTkTabview(self)
        self.tabview.pack(expand=True, fill='both', padx=10, pady=10)

        self.tabview.add('Opções')
        tab_opcoes = self.tabview.tab('Opções')
        tab_opcoes.columnconfigure((0, 1, 2), weight=1)

        self.create_tab_opcoes_widgets(tab_opcoes)

        self.tabview.add('Ajuda')
        tab_ajuda = self.tabview.tab('Ajuda')

        self.create_tab_ajuda_widgets(tab_ajuda)

    def create_tab_opcoes_widgets(self, tabela):
        frame_arquivos = CTkFrame(tabela)
        frame_arquivos.grid(row=0, column=0, padx=10, pady=10)

        CTkLabel(frame_arquivos, text='Arquivo').grid(row=0, column=0, columnspan=2)

        CTkButton(frame_arquivos, text='Abrir',
                  command=self.abrir).grid(row=1, column=0, padx=10, pady=10)

        CTkButton(frame_arquivos, text='Criar novo',
                  command=self.salvar_como).grid(row=1, column=1, padx=10, pady=10)

        frame_unidade = CTkScrollableFrame(tabela, label_text='Unidade padrão')
        frame_unidade.grid(row=0, column=1, rowspan=2, ipady=60, pady=(10, 0))
        for indice, unidade in enumerate(self.__master.unidades):
            CTkRadioButton(frame_unidade, text=unidade, value=unidade, variable=self.__master.var_nova_unidade_padrao,
                           command=self.altera_unidade_padrao).pack(ipadx=10, padx=5, pady=(0, 5), anchor='e', fill='x')

        self.__master.var_nova_unidade_padrao.set(self.__master.configuracao_unidade_padrao)

        frame_configs = CTkFrame(tabela)
        frame_configs.grid(row=1, column=0, pady=(30, 0))
        frame_configs.columnconfigure(0, weight=2)
        CTkLabel(frame_configs, text='Configurações gerais',
                 **self.__master.label_configs).grid(row=0, column=0, padx=20)

        CTkLabel(frame_configs, text='Apagar enunciado ao salvar',
                 **self.__master.label_configs).grid(row=1, column=0, padx=20, pady=(10, 0))
        CTkSwitch(frame_configs, variable=self.__master.var_apagar_enunciado, text='',
                  command=self.altera_opcao_apagar_enunciado).grid(row=2, column=0, padx=20, sticky='e')
        self.__master.var_apagar_enunciado.set(self.__master.perfil_apagar_enunciado)

        CTkLabel(frame_configs, text='Dark mode',
                 **self.__master.label_configs).grid(row=3, column=0, padx=20, pady=(10, 0))
        CTkOptionMenu(frame_configs, values=["Light", "Dark", "System"], variable=self.__master.var_dark_mode,
                      command=self.altera_dark_mode).grid(row=4, column=0, padx=20)
        self.__master.var_dark_mode.set(self.__master.perfil_aparencia_do_sistema)

        CTkLabel(frame_configs, text='Escala do sistema', **self.__master.label_configs).grid(row=5, column=0, padx=20,
                                                                                              pady=(10, 0))
        porcentagens = ["80%", "90%", "100%", "110%", "120%"]
        CTkOptionMenu(frame_configs, values=porcentagens, variable=self.__master.var_escala_do_sistema,
                      command=self.altera_escala_do_sistema).grid(row=6, column=0, padx=20, pady=(0, 20))
        self.__master.var_escala_do_sistema.set(self.__master.perfil_escala_do_sistema)

    def create_tab_ajuda_widgets(self, tabela):
        frame_atalhos = CTkScrollableFrame(tabela, height=260)
        frame_atalhos.pack(fill='both', expand=True, padx=20, pady=(0, 10))
        frame_atalhos.columnconfigure((0, 1), weight=1)
        posicao = {'padx': 2, 'pady': 5}
        for i, informacoes_atalho in enumerate(SHORTCUTS):
            descricao, atalho = informacoes_atalho
            CTkLabel(frame_atalhos, text=descricao,
                     **self.__master.label_configs).grid(column=0, row=i, sticky='e', **posicao)
            CTkLabel(frame_atalhos, text=atalho,
                     **self.__master.label_configs).grid(column=1, row=i, sticky='w', **posicao)

        frame_versao = CTkFrame(tabela, height=32)
        frame_versao.pack(fill='both', expand=True, padx=20, pady=(0, 10))
        frame_versao.columnconfigure((0, 1), weight=1)
        frame_versao.rowconfigure(0, weight=3)
        CTkLabel(frame_versao, **self.__master.label_configs,
                 text=f'Versão: {self.__master.__version__}').grid(row=0, column=0)
        CTkButton(frame_versao, text='Verificar atualização',
                  command=self.__master.verifica_atualizacao).grid(row=0, column=1)

        frame_feedback = CTkFrame(tabela, height=32)
        frame_feedback.pack(fill='both', expand=True, padx=20, pady=(0, 10))
        frame_feedback.rowconfigure(0, weight=1)
        frame_feedback.columnconfigure(0, weight=1)
        CTkButton(frame_feedback, text='Enviar feedback', width=700, height=32, anchor='center',
                  command=self.abre_feedback).grid(row=0, column=0, padx=10)

    def abrir(self):
        self.__master.abrir()
        self.destroy()

    def salvar_como(self):
        self.__master.salvar_como()
        self.destroy()

    def altera_unidade_padrao(self):
        self.__master.altera_unidade_padrao()
        self.focus()

    def altera_opcao_apagar_enunciado(self):
        self.__master.altera_opcao_apagar_enunciado()
        self.focus()

    def altera_dark_mode(self, modo: str):
        self.__master.altera_dark_mode(modo)
        self.focus()

    def altera_escala_do_sistema(self, nova_escala):
        self.__master.altera_escala_do_sistema(nova_escala)
        self.focus()

    @staticmethod
    def abre_feedback():
        call(f'start {LINK_FEEDBACK_FORM}', shell=True, stdout=False)

    def focus(self):
        self.__master.after(300, self.focus_force)

    def abre_ajuda(self):
        self.tabview.set('Ajuda')
