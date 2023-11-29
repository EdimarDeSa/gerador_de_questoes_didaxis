from pathlib import Path

from customtkinter import (
    BOTH,
    CENTER,
    CTk,
    CTkButton,
    CTkTabview,
    CTkToplevel,
    StringVar,
)

from src.Constants import GRAY, GREEN, TABAJUDA, TABOPCAO
from src.Contracts.controller import ControllerHandlers
from src.DataModels.imagemodel import ImageModel
from src.DataModels.topleveltoolsmodel import TopLevelToolsModel
from src.DataModels.usermodel import UserModel
from src.DataModels.widgetssettingsmodel import WidgetsSettingsModel

from .SetupViews import (
    CategorySelectionFrame,
    FilesFrame,
    GeneralPramsFrame,
    ShortcutsFrame,
    VersionFrame,
)


class SetupTopLevel(CTkToplevel):
    def __init__(
        self,
        master: CTk,
        widget_settings: WidgetsSettingsModel,
        topleveltools: TopLevelToolsModel,
        controller: ControllerHandlers,
        user_settings: UserModel,
        system_images: ImageModel,
        icon_path: Path,
    ):
        super().__init__(master)
        self.widget_settings = widget_settings
        self.topleveltools = topleveltools
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
        width, height = 750, 600
        pos_x = (self.winfo_screenwidth() - width) // 2
        pos_y = (self.winfo_screenheight() - height) // 2
        self.geometry(f'{width}x{height}+{pos_x}+{pos_y}')

        self.resizable(False, False)

        self.wm_iconbitmap(default=self.icon_path)

    def _setup_variables(self):
        self.var_escala_do_sistema = StringVar(value=self.user_settings.user_scaling)
        self.var_aparencia_do_sistema = StringVar(
            value=self.user_settings.user_appearance_mode
        )

    def _setup_ui(self):
        self.tabview = CTkTabview(self)
        self.tabview.pack(expand=True, fill=BOTH, padx=10, pady=10)

        tab_opcoes = self.tabview.add(TABOPCAO)
        for i in range(3):
            tab_opcoes.grid_columnconfigure(i, weight=1)
        self.create_tab_opcoes_widgets(tab_opcoes)

        tab_ajuda = self.tabview.add(TABAJUDA)
        self.create_tab_ajuda_widgets(tab_ajuda)

    def create_tab_opcoes_widgets(self, master):
        FilesFrame(
            master,
            self.widget_settings.label_settings,
            self.widget_settings.button_default_settings,
            self.topleveltools.new_db,
            self.topleveltools.open_db,
            self.topleveltools.export_db,
            fg_color=GRAY,
        ).grid(row=0, column=0, padx=10, pady=10)

        CategorySelectionFrame(
            master,
            self.widget_settings.button_default_settings,
            self.user_settings.category_options,
            self.topleveltools.category,
            self.category_change_handler,
            fg_color=GRAY,
            **self.widget_settings.scrollable_label_settings,
        ).grid(row=0, column=1, rowspan=2, ipady=90, pady=(10, 0))

        GeneralPramsFrame(
            master,
            self.widget_settings.label_settings,
            self.controller.update_user_settings_handler,
            self.topleveltools.var_erase_statement,
            self.topleveltools.var_auto_export,
            self.var_aparencia_do_sistema,
            self.topleveltools.set_appearance,
            self.var_escala_do_sistema,
            self.topleveltools.set_scaling,
            fg_color=GRAY,
        ).grid(row=1, column=0, pady=(30, 0))

    def create_tab_ajuda_widgets(self, tabela):
        ShortcutsFrame(
            tabela,
            self.widget_settings.label_settings,
            fg_color=GRAY,
            height=260,
        ).pack(fill=BOTH, expand=True, padx=20, pady=(0, 10))

        CTkButton(
            tabela,
            text='Enviar feedback',
            width=700,
            height=32,
            border_color=GREEN,
            border_width=2,
            fg_color='transparent',
            anchor=CENTER,
            command=self.controller.send_feedback_handler,
            **self.widget_settings.button_title_settings,
        ).pack(fill=BOTH, expand=True, padx=20, pady=(0, 10))

        VersionFrame(
            tabela,
            self.widget_settings.label_settings,
            self.controller.get_version,
            self.controller.__version__,
            height=32,
        ).pack(fill=BOTH, expand=True, padx=20, pady=(0, 10))

    def category_change_handler(self):
        self.controller.update_user_settings_handler(
            user_default_category=self.topleveltools.category.get()
        )

    def open_help_tab(self) -> None:
        self.wm_deiconify()
        self.tabview.set(TABAJUDA)

    def close_window_event(self) -> None:
        self.tabview.set(TABOPCAO)
        self.withdraw()
