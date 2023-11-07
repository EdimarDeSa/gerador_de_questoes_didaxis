from customtkinter import CTkButton, CTkFrame, CTkLabel, CTkToplevel

from src.Hints.hints import MenuSettingsHint, Callable


class VersionFrame(CTkFrame):
    __version__ = None

    def __init__(
            self,
            master: CTkToplevel,
            label_configs: MenuSettingsHint,
            version_verify: Callable,
            **kwargs
    ):
        super().__init__(master, **kwargs)

        self.get_project_version()

        self.version_verify = version_verify

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=3)

        # TODO: Implementar atualização
        CTkLabel(
            self, text=f'Versão: {self.__version__}', **label_configs
        ).grid(row=0, column=0)
        CTkButton(self, text='Verificar atualização', command=self.check_verify).grid(
            row=0, column=1
        )

    def check_verify(self):
        new_version = self.version_verify()
        print(new_version)

    @classmethod
    def get_project_version(cls):
        import tomllib

        with open('./pyproject.toml', 'rb') as file:
            pyproject_data = tomllib.load(file)

        cls.__version__ = pyproject_data['tool']['poetry']['version']
