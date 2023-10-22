from typing import Literal

from customtkinter import *
from back_end import API
from FrontEndFunctions.Constants import SHORTCUTS, APARENCIAS_DO_SISTEMA, PORCENTAGENS


class SetupFrame(CTkToplevel):
    def __init__(self, master: CTk, api: API, **kwargs):
        super().__init__(master=master, **kwargs)

        self._api = api

        self._var_auto_clean_on_off = StringVar()
        self._var_auto_export_on_off = StringVar()

        self._configura_tela()

        # self._set_ui()

        self.protocol('WM_DELETE_WINDOW', self.close_window_event)

    def _configura_tela(self):
        largura, altura = 750, 500
        pos_x = (self.winfo_screenwidth() - largura) // 2
        pos_y = (self.winfo_screenheight() - altura) // 2

        self.geometry(f'{largura}x{altura}+{pos_x}+{pos_y}')
        self.resizable(False, False)
        self.withdraw()

    def _set_ui(self):
        self.tabview = CTkTabview(self)
        self.tabview.pack(expand=True, fill=BOTH, padx=10, pady=10)
        self.tabview.add('Opções')
        self.tabview.add('Ajuda')

        tab_opcoes = self.tabview.tab('Opções')
        for i in range(3): tab_opcoes.grid_columnconfigure(i, weight=1)
        self.create_tab_opcoes_widgets(tab_opcoes)

        tab_ajuda = self.tabview.tab('Ajuda')
        self.create_tab_ajuda_widgets(tab_ajuda)

    def create_tab_opcoes_widgets(self, master):
        pad = dict(padx=10, pady=10)
        frame_arquivos = CTkFrame(master)
        frame_arquivos.grid(row=0, column=0, **pad)

        CTkLabel(frame_arquivos, text='Arquivo').grid(row=0, column=0, columnspan=2)

        CTkButton(frame_arquivos, text='Abrir', command=self._api.open_db_handler).grid(row=1, column=0, **pad)

        CTkButton(frame_arquivos, text='Criar novo', command=self._api.export_handler).grid(row=1, column=1, **pad)

        frame_unidade = CTkScrollableFrame(master, label_text='Unidade padrão')
        frame_unidade.grid(row=0, column=1, rowspan=2, ipady=90, pady=(10, 0))
        for indice, unidade in enumerate(self._api.category_list):
            CTkRadioButton(
                frame_unidade, text=unidade, value=unidade, variable=self._api.categoria,
                command=self._api.type_change_handler
            ).pack(ipadx=10, padx=5, pady=(0, 5), fill=BOTH)

        frame_configs = CTkFrame(master)
        frame_configs.grid(row=1, column=0, pady=(30, 0))

        position_top = dict(padx=10, anchor=CENTER, expand=True)
        position_bottom = dict(padx=10, pady=(0, 20), anchor=CENTER, expand=True)

        CTkLabel(frame_configs, text='Configurações gerais', **self._api.label_configs).pack(**position_bottom)

        CTkLabel(frame_configs, text='Apagar enunciado ao salvar?', **self._api.label_configs).pack(**position_top)

        # noinspection PyTypeChecker
        CTkSwitch(
            frame_configs, variable=self._api.var_apagar_enunciado, text=None, width=0, switch_width=75,
            command=self.altera_opcao_apagar_enunciado, textvariable=self._var_auto_clean_on_off
        ).pack(**position_bottom)
        self.altera_opcao_apagar_enunciado()

        CTkLabel(frame_configs, text='Exportar automaticamente?', **self._api.label_configs).pack(**position_top)
        CTkSwitch(
            frame_configs, variable=self._api.var_auto_export, text=None, width=0, switch_width=75,
            command=self.altera_opcao_auto_exportar, textvariable=self._var_auto_export_on_off
        ).pack(**position_bottom)
        self.altera_opcao_auto_exportar()

        CTkLabel(frame_configs, text='Dark mode', **self._api.label_configs).pack(**position_top)
        CTkOptionMenu(frame_configs, values=APARENCIAS_DO_SISTEMA, variable=self._api.var_aparencia_do_sistema,
                      command=self.salva_e_altera_aparencia).pack(**position_bottom)

        CTkLabel(
            frame_configs, text='Escala do sistema', **self.cnf_manager.label_titulos_configs
        ).pack(**position_top)
        CTkOptionMenu(frame_configs, values=PORCENTAGENS, variable=self.gvar.var_escala_do_sistema,
                      command=self.salva_e_altera_escala_do_sistema).pack(**position_bottom)

    def create_tab_ajuda_widgets(self, tabela):
        frame_atalhos = CTkScrollableFrame(tabela, height=260)
        frame_atalhos.pack(fill=BOTH, expand=True, padx=20, pady=(0, 10))
        frame_atalhos.columnconfigure(0, weight=1)
        frame_atalhos.columnconfigure(1, weight=2)
        pad = dict(padx=2, pady=5)

        for i, informacoes_atalho in enumerate(SHORTCUTS):
            descricao, atalho = informacoes_atalho
            CTkLabel(
                frame_atalhos, text=descricao, **self.cnf_manager.label_titulos_configs
            ).grid(column=0, row=i, sticky=E, **pad)

            CTkLabel(
                frame_atalhos, text=atalho, **self.cnf_manager.label_titulos_configs
            ).grid(column=1, row=i, sticky=W, **pad)

        frame_versao = CTkFrame(tabela, height=32)
        frame_versao.pack(fill=BOTH, expand=True, padx=20, pady=(0, 10))
        frame_versao.columnconfigure(0, weight=1)
        frame_versao.columnconfigure(1, weight=1)
        frame_versao.rowconfigure(0, weight=3)

        CTkLabel(
            frame_versao, text=f'Versão: {__version__}', **self.cnf_manager.label_titulos_configs
        ).grid(row=0, column=0)
        CTkButton(frame_versao, text='Verificar atualização', command='self.verifica_atualizacao').grid(row=0, column=1)

        CTkButton(
            tabela, text='Enviar feedback', width=700, height=32, border_color=VERDE, border_width=2,
            fg_color=TRANSPARENTE, anchor=CENTER, command=abre_feedback, **self.cnf_manager.buttons_configs
        ).pack(fill=BOTH, expand=True, padx=20, pady=(0, 10))

    def abrir(self):
        arquivo = AbrirArquivo().serialized_questions
        self.destroy()

    def salvar_como(self):
        self.gvar.arquivos.salvar_como()
        self.destroy()

    def altera_opcao_apagar_enunciado(self):
        apagar = 'DESLIGADO'
        if self._api.var_apagar_enunciado.get(): apagar = 'LIGADO'
        self._var_auto_clean_on_off.set(apagar)

        self._api.salva_informacao_perfil('apagar_enunciado', self.gvar.var_apagar_enunciado.get())
        self.focus()

    def altera_opcao_auto_exportar(self):
        apagar = 'DESLIGADO'
        if self.gvar.var_auto_export.get():
            apagar = 'LIGADO'
        self._var_auto_export_on_off.set(apagar)

        self.gvar.perfil.salva_informacao_perfil('exportar_automaticamente', self.gvar.var_apagar_enunciado.get())
        self.focus()

    def salva_e_altera_aparencia(self, config: Literal['system', 'dark', 'light']):
        self.gvar.perfil.salva_informacao_perfil('dark_mode', config)
        altera_aparencia(config)
        self.focus()

    def salva_e_altera_escala_do_sistema(self, nova_escala):
        self.gvar.perfil.salva_informacao_perfil('var_escala_do_sistema', nova_escala)
        altera_escala(nova_escala)
        self.focus()

    def focus(self):
        self.after(100, self.focus_force)

    def abre_ajuda(self):
        self.tabview.set('Ajuda')

    def close_window_event(self):
        self.withdraw()