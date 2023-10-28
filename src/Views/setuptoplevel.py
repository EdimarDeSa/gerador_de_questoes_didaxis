from pathlib import Path

from customtkinter import CTk, CTkToplevel, StringVar, CTkTabview, BOTH, CTkButton, CENTER

from src.contracts.controller import ControllerHandlers
from src.contracts.viewcontract import ViewContract

from .SetupViews import FilesFrame, CategorySelectionFrame, GeneralPramsFrame, ShortcutsFrame, VersionFrame
from src.Hints import UserSetHint, SysImgHint
from src.Constants import TABAJUDA, TABOPCAO, GRAY, GREEN


class SetupTopLevel(CTkToplevel):
    def __init__(self, master: CTk, ctkview: ViewContract, controller: ControllerHandlers, user_settings: UserSetHint,
                 system_images: SysImgHint, icon_path: Path):
        super().__init__(master)
        self.ctkview = ctkview
        self.controller = controller
        self.user_settings = user_settings
        self.system_images = system_images
        self.icon_path = icon_path

        self._setup_window()
        self._setup_variables()
        self._setup_ui()

        self.protocol('WM_DELETE_WINDOW', self.close_window_event)

        # self.withdraw()

    def _setup_window(self):
        largura, altura = 750, 600
        pos_x = (self.winfo_screenwidth() - largura) // 2
        pos_y = (self.winfo_screenheight() - altura) // 2

        self.geometry(f'{largura}x{altura}+{pos_x}+{pos_y}')
        self.resizable(False, False)
        self.wm_iconbitmap(default=self.icon_path)

    def _setup_variables(self):
        self.var_escala_do_sistema = StringVar(value=self.user_settings['user_scaling'])
        self.var_aparencia_do_sistema = StringVar(value=self.user_settings['user_appearance_mode'])

    def _setup_ui(self):
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
            master, self.ctkview.label_settings, self.ctkview.button_default_settings,
            self.ctkview.new_db, self.ctkview.open_db, self.ctkview.export_db, fg_color=GRAY
        ).grid(row=0, column=0, padx=10, pady=10)

        CategorySelectionFrame(
            master, self.ctkview.button_default_settings, self.ctkview.category_options,
            self.ctkview.category, self.category_change_handler,
            fg_color=GRAY, **self.ctkview.scrollable_label_settings
        ).grid(row=0, column=1, rowspan=2, ipady=90, pady=(10, 0))

        GeneralPramsFrame(
            master, self.ctkview.label_settings, self.controller.update_user_settings_handler,
            self.ctkview.var_erase_statement, self.ctkview.var_auto_export,
            self.var_aparencia_do_sistema, self.ctkview.set_appearance,
            self.var_escala_do_sistema, self.ctkview.set_scaling, fg_color=GRAY
        ).grid(row=1, column=0, pady=(30, 0))

    def create_tab_ajuda_widgets(self, tabela):
        ShortcutsFrame(
            tabela, self.ctkview.label_settings, fg_color=GRAY, height=260
        ).pack(fill=BOTH, expand=True, padx=20, pady=(0, 10))

        VersionFrame(tabela, self.ctkview.label_settings, height=32).pack(fill=BOTH, expand=True, padx=20, pady=(0, 10))

        CTkButton(
            tabela, text='Enviar feedback', width=700, height=32, border_color=GREEN, border_width=2,
            fg_color='transparent', anchor=CENTER, command=self.controller.send_feedback_handler,
            **self.ctkview.button_title_settings
        ).pack(fill=BOTH, expand=True, padx=20, pady=(0, 10))

    def category_change_handler(self):
        self.controller.update_user_settings_handler('user_default_category', self.ctkview.category.get())

    def open_help_tab(self) -> None:
        self.wm_deiconify()
        self.tabview.set(TABAJUDA)

    def close_window_event(self) -> None:
        self.tabview.set(TABOPCAO)
        self.withdraw()
