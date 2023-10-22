from customtkinter import CTkFrame, CTk, CTkButton, LEFT, X

from ..Hints import ConfigsHint, ImageHint, ShowWindowHandler, ExportHandler, SaveQuestionHandler


class CommandButtonsFrame(CTkFrame):
    def __init__(
            self, master: CTk, img_config: ImageHint, buttons_configs: ConfigsHint,
            configs_window_handler: ShowWindowHandler, export_handler: ExportHandler,
            save_question_handler: SaveQuestionHandler, **kwargs
    ):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=3)
        
        positioning = dict(expand=True, side=LEFT)

        # noinspection PyTypeChecker
        CTkButton(
            self, text=None, width=60, height=32, image=img_config, command=configs_window_handler, **buttons_configs
        ).pack(**positioning)
        
        positioning.update(dict(fill=X, padx=(0, 10)))
        
        CTkButton(
            self, text='Exportar', width=300, height=32, command=export_handler, **buttons_configs
        ).pack(**positioning)

        self.bt_salvar = CTkButton(
            self, text='Salvar', width=300, height=32, command=save_question_handler, **buttons_configs
        )
        self.bt_salvar.pack(**positioning)
