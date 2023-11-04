from customtkinter import CTkButton, CTkFrame, CTkLabel, CTkToplevel

from src.Hints.hints import MenuSettingsHint


class VersionFrame(CTkFrame):
    __version__ = None

    def __init__(
        self, master: CTkToplevel, label_configs: MenuSettingsHint, **kwargs
    ):
        super().__init__(master, **kwargs)

        self.get_project_version()

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=3)

        # TODO: Implementar atualização
        CTkLabel(
            self, text=f'Versão: {self.__version__}', **label_configs
        ).grid(row=0, column=0)
        CTkButton(self, text='Verificar atualização', command=self).grid(
            row=0, column=1
        )

    @classmethod
    def get_project_version(cls):
        import tomllib

        with open('./pyproject.toml', 'rb') as file:
            pyproject_data = tomllib.load(file)

        cls.__version__ = pyproject_data['tool']['poetry']['version']
