from tkinter.messagebox import askyesno
from typing import Literal

from Modules import __version__
from Modules.atualizacao import Atualizacao
from Modules.models.globalvars import *
from Modules.funcoes.aparencia import altera_aparencia, altera_escala
from Modules.funcoes import abrir, get_desktop_path, abre_feedback


class JanelaDeConfiguracoes(CTkToplevel):
    def __init__(self, master, variaveis_globais: VariaveisGlobais, **kwargs):
        super().__init__(master=master, **kwargs)

        self.gvar = variaveis_globais
        self.var_escala_do_sistema = StringVar(value=self.gvar.perfil.escala_do_sistema)
        self.var_auto_clean_on_off = StringVar(value='ON')
        self.var_auto_export_on_off = StringVar(value='ON')

        self.atualizador = Atualizacao(__version__, self.gvar.arquivos.base_dir)
        self.configura_tela()

        self._init_tabela()
        self.focus()

    def configura_tela(self):
        largura, altura = 700, 500
        pos_x = (self.winfo_screenwidth() - largura) // 2
        pos_y = (self.winfo_screenheight() - altura) // 2

        self.geometry(f'{largura}x{altura}+{pos_x}+{pos_y}')
        self.resizable(OFF, OFF)

    def _init_tabela(self):
        self.tabview = CTkTabview(self)
        self.tabview.pack(expand=ON, fill=BOTH, padx=10, pady=10)

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

        frame_configs = CTkFrame(master)
        frame_configs.grid(row=1, column=0, pady=(30, 0))

        position_top = dict(padx=10, anchor=CENTER, expand=ON)
        position_bottom = dict(padx=10, pady=(0, 20), anchor=CENTER, expand=ON)

        CTkLabel(
            frame_configs, text='Configurações gerais', **self.gvar.configs.label_titulos_configs
        ).pack(**position_bottom)

        CTkLabel(
            frame_configs, text='Apagar enunciado ao salvar?', **self.gvar.configs.label_titulos_configs
        ).pack(**position_top)
        # noinspection PyTypeChecker
        CTkSwitch(
            frame_configs, variable=self.gvar.var_apagar_enunciado, text=None, width=0, switch_width=75,
            command=self.altera_opcao_apagar_enunciado, textvariable=self.var_auto_clean_on_off
        ).pack(**position_bottom)

        CTkLabel(
            frame_configs, text='Exportar automaticamente?', **self.gvar.configs.label_titulos_configs
        ).pack(**position_top)
        # noinspection PyTypeChecker
        CTkSwitch(
            frame_configs, variable=self.gvar.var_exportar_automaticamente, text=None, width=0, switch_width=75,
            command=self.altera_opcao_auto_exportar, textvariable=self.var_auto_export_on_off
        ).pack(**position_bottom)

        CTkLabel(frame_configs, text='Dark mode', **self.gvar.configs.label_titulos_configs).pack(**position_top)
        # noinspection PyTypeChecker
        CTkOptionMenu(
            frame_configs, values=APARENCIAS_DO_SISTEMA, variable=self.gvar.var_dark_mode,
            command=self.salva_e_altera_aparencia
        ).pack(**position_bottom)

        CTkLabel(
            frame_configs, text='Escala do sistema', **self.gvar.configs.label_titulos_configs
        ).pack(**position_top)
        CTkOptionMenu(
            frame_configs, values=PORCENTAGENS, variable=self.var_escala_do_sistema,
            command=self.salva_e_altera_escala_do_sistema
        ).pack(**position_bottom)

    def create_tab_ajuda_widgets(self, tabela):
        frame_atalhos = CTkScrollableFrame(tabela, height=260)
        frame_atalhos.pack(fill=BOTH, expand=ON, padx=20, pady=(0, 10))
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
        frame_versao.pack(fill=BOTH, expand=ON, padx=20, pady=(0, 10))
        frame_versao.columnconfigure(0, weight=1)
        frame_versao.columnconfigure(1, weight=1)
        frame_versao.rowconfigure(0, weight=3)

        CTkLabel(
            frame_versao, text=f'Versão: {__version__}', **self.gvar.configs.label_titulos_configs
        ).grid(row=0, column=0)
        CTkButton(frame_versao, text='Verificar atualização', command=self.verifica_atualizacao).grid(row=0, column=1)

        CTkButton(
            tabela, text='Enviar feedback', width=700, height=32, border_color=VERDE, border_width=2,
            fg_color=TRANSPARENTE, anchor=CENTER, command=abre_feedback, **self.gvar.configs.buttons_configs
        ).pack(fill=BOTH, expand=ON, padx=20, pady=(0, 10))

    def abrir(self):
        abrir()
        self.destroy()

    def salvar_como(self):
        self.gvar.arquivos.salvar_como()
        self.destroy()

    def altera_unidade_padrao(self):
        self.gvar.perfil.salva_informacao_perfil('unidade_padrao', self.gvar.var_unidade_padrao.get())
        self.focus()

    def altera_opcao_apagar_enunciado(self):
        apagar = 'DESLIGADO'
        if self.gvar.var_apagar_enunciado.get():
            apagar = 'LIGADO'
        self.var_auto_clean_on_off.set(apagar)

        self.gvar.perfil.salva_informacao_perfil('apagar_enunciado', self.gvar.var_apagar_enunciado.get())
        self.focus()

    def altera_opcao_auto_exportar(self):
        apagar = 'DESLIGADO'
        if self.gvar.var_exportar_automaticamente.get():
            apagar = 'LIGADO'
        self.var_auto_export_on_off.set(apagar)

        self.gvar.perfil.salva_informacao_perfil('exportar_automaticamente', self.gvar.var_apagar_enunciado.get())
        self.focus()

    def salva_e_altera_aparencia(self, config: Literal['system', 'dark', 'light']):
        self.gvar.perfil.salva_informacao_perfil('dark_mode', config)
        altera_aparencia(config)
        self.focus()

    def salva_e_altera_escala_do_sistema(self, nova_escala):
        self.gvar.perfil.salva_informacao_perfil('escala_do_sistema', nova_escala)
        altera_escala(nova_escala)
        self.focus()

    def focus(self):
        self.after(100, self.focus_force)

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
            self.gvar.exit()
