from customtkinter import *

from back_end import Controller
from .SetupFrames import *
from .Constants import GRAY, TABOPCAO, TABAJUDA, TRANSPARENTE, VERDE


class SetupTopLevel(CTkToplevel):
    def __init__(self, master: CTk, api: Controller, **kwargs):
        super().__init__(master=master, **kwargs)

        self._api = api

        self._configura_tela()

        self._set_ui()

        self.protocol('WM_DELETE_WINDOW', self.close_window_event)

    def _configura_tela(self):
        largura, altura = 750, 600
        pos_x = (self.winfo_screenwidth() - largura) // 2
        pos_y = (self.winfo_screenheight() - altura) // 2

        self.geometry(f'{largura}x{altura}+{pos_x}+{pos_y}')
        self.resizable(False, False)
        self.withdraw()

    def _set_ui(self):
        self.tabview = CTkTabview(self)
        self.tabview.pack(expand=True, fill=BOTH, padx=10, pady=10)

        self.tabview.add(TABOPCAO)
        tab_opcoes = self.tabview.tab(TABOPCAO)
        for i in range(3): tab_opcoes.grid_columnconfigure(i, weight=1)
        self.create_tab_opcoes_widgets(tab_opcoes)

        self.tabview.add(TABAJUDA)
        tab_ajuda = self.tabview.tab(TABAJUDA)
        self.create_tab_ajuda_widgets(tab_ajuda)

    def create_tab_opcoes_widgets(self, master):
        FilesFrame(
            master, self._api.open_db_handler, self._api.export_handler,
            fg_color=GRAY
        ).grid(row=0, column=0, padx=10, pady=10)

        CategorySelectionFrame(
            master, self._api.category_list, self._api.categoria,
            self._api.category_change_handler, fg_color=GRAY
        ).grid(row=0, column=1, rowspan=2, ipady=90, pady=(10, 0))

        GeneralPramsFrame(
            master, self._api.label_configs, self._api.save_new_config_handler,
            self._api.var_erase_statement, self._api.var_auto_export,
            self._api.var_aparencia_do_sistema, self._api.change_appearance_handler,
            self._api.var_escala_do_sistema, self._api.change_scale_handler, fg_color=GRAY
        ).grid(row=1, column=0, pady=(30, 0))

    def create_tab_ajuda_widgets(self, tabela):
        ShortcutsFrame(
            tabela, self._api.label_configs, fg_color=GRAY, height=260
        ).pack(fill=BOTH, expand=True, padx=20, pady=(0, 10))

        VersionFrame(tabela, self._api.label_configs, height=32).pack(fill=BOTH, expand=True, padx=20, pady=(0, 10))

        CTkButton(
            tabela, text='Enviar feedback', width=700, height=32, border_color=VERDE, border_width=2,
            fg_color=TRANSPARENTE, anchor=CENTER, command=self._api, **self._api.button_configs
        ).pack(fill=BOTH, expand=True, padx=20, pady=(0, 10))

    def abre_ajuda(self) -> None:
        self.wm_deiconify()
        self.tabview.set(TABAJUDA)

    def close_window_event(self) -> None:
        self.tabview.set(TABOPCAO)
        self.withdraw()
