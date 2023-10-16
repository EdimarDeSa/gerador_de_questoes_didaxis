from subprocess import call

from Modules.atualizacao import *
from Modules.constants import __version__
from Modules.models.globalvars import *


class PainelDeConfiguracoes(CTkToplevel):
    def __init__(self, master, variaveis_globais: VariaveisGlobais, **kwargs):
        super().__init__(master=master, **kwargs)

        self.gvar = variaveis_globais
        self.var_escala_do_sistema = StringVar()

        self.atualizador = Atualizacao(__version__, self.gvar.arquivos.BASE)
        self.configura_tela()

        self._init_tabela()
        self.focus()

    def configura_tela(self):
        largura, altura = (700, 500)
        pos_x = (self.winfo_screenwidth() - largura) // 2
        pos_y = (self.winfo_screenheight() - altura) // 2

        self.geometry(f'700x500+{pos_x}+{pos_y}')
        self.resizable(False, False)

    def _init_tabela(self):
        self.tabview = CTkTabview(self)
        self.tabview.pack(expand=True, fill=BOTH, padx=10, pady=10)

        self.tabview.add('Opções')
        tab_opcoes = self.tabview.tab('Opções')
        tab_opcoes.columnconfigure(0, weight=1)
        tab_opcoes.columnconfigure(1, weight=1)
        tab_opcoes.columnconfigure(2, weight=1)

        self.create_tab_opcoes_widgets(tab_opcoes)

        self.tabview.add('Ajuda')
        tab_ajuda = self.tabview.tab('Ajuda')

        self.create_tab_ajuda_widgets(tab_ajuda)

    def create_tab_opcoes_widgets(self, master):
        pad = dict(padx=10, pady=10)
        frame_arquivos = CTkFrame(master)
        frame_arquivos.grid(row=0, column=0, **pad)

        CTkLabel(frame_arquivos, text='Arquivo').grid(row=0, column=0, columnspan=2)

        CTkButton(frame_arquivos, text='Abrir', command=self.abrir).grid(row=1, column=0, **pad)

        CTkButton(frame_arquivos, text='Criar novo', command=self.salvar_como).grid(row=1, column=1, **pad)

        frame_unidade = CTkScrollableFrame(master, label_text='Unidade padrão')
        frame_unidade.grid(row=0, column=1, rowspan=2, ipady=90, pady=(10, 0))
        for indice, unidade in enumerate(self.gvar.configs.unidades):
            CTkRadioButton(
                frame_unidade, text=unidade, value=unidade, variable=self.gvar.var_unidade_padrao,
                command=self.altera_unidade_padrao
            ).pack(ipadx=10, padx=5, pady=(0, 5), fill=BOTH)

        self.gvar.var_unidade_padrao.set(self.gvar.perfil.unidade_padrao)

        frame_configs = CTkFrame(master)
        frame_configs.grid(row=1, column=0, pady=(30, 0))
        CTkLabel(
            frame_configs, text='Configurações gerais', **self.gvar.configs.label_titulos_configs
        ).grid(row=0, column=0, padx=20)

        CTkLabel(
            frame_configs, text='Apagar enunciado ao salvar', **self.gvar.configs.label_titulos_configs
        ).grid(row=1, column=0, padx=20, pady=(10, 0))

        CTkSwitch(
            frame_configs, variable=self.gvar.var_apagar_enunciado, text=None, command=self.altera_opcao_apagar_enunciado
        ).grid(row=2, column=0, padx=20, sticky=E)

        self.gvar.var_apagar_enunciado.set(self.gvar.perfil.apagar_enunciado)

        CTkLabel(frame_configs, text='Dark mode',
                 **self.gvar.configs.label_titulos_configs).grid(row=3, column=0, padx=20, pady=(10, 0))
        CTkOptionMenu(
            frame_configs, values=APARENCIAS_DO_SISTEMA, variable=self.gvar.var_dark_mode, command=self.altera_dark_mode
        ).grid(row=4, column=0, padx=20)

        self.gvar.var_dark_mode.set(self.gvar.perfil.aparencia_do_sistema)

        CTkLabel(
            frame_configs, text='Escala do sistema', **self.gvar.configs.label_titulos_configs
        ).grid(row=5, column=0, padx=20, pady=(10, 0))
        CTkOptionMenu(
            frame_configs, values=PORCENTAGENS, variable=self.var_escala_do_sistema,
            command=self.gvar.altera_escala_do_sistema
        ).grid(row=6, column=0, padx=20, pady=(0, 20))

        self.var_escala_do_sistema.set(self.gvar.perfil.escala_do_sistema)

    def create_tab_ajuda_widgets(self, tabela):
        frame_atalhos = CTkScrollableFrame(tabela, height=260)
        frame_atalhos.pack(fill=BOTH, expand=True, padx=20, pady=(0, 10))
        frame_atalhos.columnconfigure(0, weight=1)
        frame_atalhos.columnconfigure(1, weight=2)
        pad = dict(padx=2, pady=5)

        for i, informacoes_atalho in enumerate(SHORTCUTS):
            descricao, atalho = informacoes_atalho
            CTkLabel(
                frame_atalhos, text=descricao, **self.gvar.configs.label_titulos_configs
            ).grid(column=0, row=i, sticky=E, **pad)

            CTkLabel(
                frame_atalhos, text=atalho, **self.gvar.configs.label_titulos_configs
            ).grid(column=1, row=i, sticky=W, **pad)

        frame_versao = CTkFrame(tabela, height=32)
        frame_versao.pack(fill=BOTH, expand=True, padx=20, pady=(0, 10))
        frame_versao.columnconfigure(0, weight=1)
        frame_versao.columnconfigure(1, weight=1)
        frame_versao.rowconfigure(0, weight=3)

        CTkLabel(
            frame_versao, **self.gvar.configs.label_titulos_configs, text=f'Versão: {__version__}'
        ).grid(row=0, column=0)
        CTkButton(frame_versao, text='Verificar atualização', command=self.verifica_atualizacao).grid(row=0, column=1)

        frame_feedback = CTkFrame(tabela, height=32)
        frame_feedback.pack(fill=BOTH, expand=True, padx=20, pady=(0, 10))
        frame_feedback.rowconfigure(0, weight=1)
        frame_feedback.columnconfigure(0, weight=1)
        CTkButton(frame_feedback, text='Enviar feedback', width=700, height=32, anchor=CENTER,
                  command=self.abre_feedback).grid(row=0, column=0, padx=10)

    def abrir(self):
        self.gvar.cmd_abrir()
        self.destroy()

    def salvar_como(self):
        self.gvar.cmd_salver_como()
        self.destroy()

    def altera_unidade_padrao(self):
        self.gvar.perfil.salva_informacao_perfil('unidade_padrao', self.gvar.var_unidade_padrao.get())
        self.focus()

    def altera_opcao_apagar_enunciado(self):
        self.gvar.perfil.salva_informacao_perfil('apagar_enunciado', self.gvar.var_apagar_enunciado.get())
        self.focus()

    def altera_dark_mode(self, _):
        self.gvar.perfil.salva_informacao_perfil('dark_mode', self.gvar.var_dark_mode.get())
        set_appearance_mode(self.gvar.perfil.aparencia_do_sistema)
        self.focus()

    @staticmethod
    def abre_feedback():
        call(f'start {LINK_FEEDBACK_FORM}', shell=True, stdout=False)

    def focus(self):
        self.master.after(300, self.focus_force)

    def abre_ajuda(self):
        self.tabview.set('Ajuda')

    def verifica_atualizacao(self):
        resposta = None
        if self.atualizador.atualizacao_disponivel:
            resposta = askyesno(
                'Nova atualização disponível',
                f'O programa está atualmente na versão {__version__}.\n'
                f'A versão disponível é a {self.atualizador.versao_nova}.\n'
                f'Deseja atualizar agora?'
            )

        if resposta:
            self.atualizador.atualiza()
            self.gvar.cmd_exit()
