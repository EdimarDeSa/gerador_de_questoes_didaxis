from customtkinter import CTkFrame, CTk, CTkButton, CTkImage, NSEW, NS

from Hints import MenuSettingsHint, Callable
from Constants import DARKGRAY, BLUE, HOVER_BLUE, BORDER_BLUE


class CommandButtonsFrame(CTkFrame):
    def __init__(
            self, master: CTk, img_config: CTkImage, buttons_configs: MenuSettingsHint,
            configs_window_handler: Callable, export_handler: Callable, save_question_handler: Callable
    ):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=10)
        self.grid_columnconfigure(2, weight=10)
        self.grid_rowconfigure(0, weight=1)

        CTkButton(
            self, text=None, fg_color=DARKGRAY, image=img_config, command=configs_window_handler, **buttons_configs
        ).grid(column=0, row=0, sticky=NS, padx=(10, 0), pady=5)

        CTkButton(
            self, text='Exportar', fg_color=BLUE, hover_color=HOVER_BLUE,
            border_color=BORDER_BLUE, command=export_handler, **buttons_configs
        ).grid(column=1, row=0, sticky=NSEW, padx=10, pady=5)

        self.b = CTkButton(
            self, text='Salvar', command=save_question_handler, **buttons_configs
        )
        self.b.grid(column=2, row=0, sticky=NSEW, padx=(0, 10), pady=5)
