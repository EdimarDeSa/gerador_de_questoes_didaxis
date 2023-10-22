from customtkinter import CTkFrame, CTkToplevel, CTkLabel, CTkSwitch, CTkOptionMenu, CENTER, StringVar

from FrontEndFunctions.Constants import APARENCIAS_DO_SISTEMA, PORCENTAGENS
from FrontEndFunctions.Hints import ConfigsHint, BooleanVarHint, StringVarHint, SaveNewConfigHint, Callable


class GeneralPramsFrame(CTkFrame):
    def __init__(
            self, master: CTkToplevel, label_configs: ConfigsHint, save_new_config_handler: SaveNewConfigHint,
            var_erase_statement: BooleanVarHint, var_auto_export: BooleanVarHint,
            var_aparencia_do_sistema: StringVarHint, change_appearance_handler: Callable,
            var_escala_do_sistema: StringVarHint, change_scale_handler: Callable, **kwargs
    ):
        super().__init__(master, **kwargs)

        self.save_new_config_handler = save_new_config_handler
        self.change_appearance_handler = change_appearance_handler
        self.change_scale_handler = change_scale_handler

        self.var_erase_statement = var_erase_statement
        self.var_auto_export = var_auto_export
        self.var_aparencia_do_sistema = var_aparencia_do_sistema
        self.var_escala_do_sistema = var_escala_do_sistema

        self._var_erase_statement_on_off = StringVar(value=self.check_state(var_erase_statement.get()))
        self._var_auto_export_on_off = StringVar(value=self.check_state(var_auto_export.get()))

        self.position_top = dict(padx=10, anchor=CENTER, expand=True)
        self.position_bottom = dict(padx=10, pady=(0, 20), anchor=CENTER, expand=True)

        self.change_erase_statement()
        self.change_auto_exportar()

        CTkLabel(self, text='Configurações gerais', **label_configs).pack(**self.position_bottom)

        CTkLabel(self, text='Apagar enunciado ao salvar?', **label_configs).pack(**self.position_top)
        # noinspection PyTypeChecker
        CTkSwitch(
            self, variable=self.var_erase_statement, text=None, width=0, switch_width=75,
            command=self.change_erase_statement, textvariable=self._var_erase_statement_on_off
        ).pack(**self.position_bottom)

        CTkLabel(self, text='Exportar automaticamente?', **label_configs).pack(**self.position_top)
        CTkSwitch(
            self, variable=self.var_auto_export, text=None, width=0, switch_width=75,
            command=self.change_auto_exportar, textvariable=self._var_auto_export_on_off
        ).pack(**self.position_bottom)

        CTkLabel(self, text='Dark mode', **label_configs).pack(**self.position_top)
        CTkOptionMenu(
            self, values=APARENCIAS_DO_SISTEMA, variable=self.var_aparencia_do_sistema,
            command=self.salva_e_altera_aparencia
        ).pack(**self.position_bottom)

        CTkLabel(self, text='Escala do sistema', **label_configs).pack(**self.position_top)
        CTkOptionMenu(
            self, values=PORCENTAGENS, variable=self.var_escala_do_sistema,
            command=self.salva_e_altera_escala_do_sistema
        ).pack(**self.position_bottom)

    def change_erase_statement(self) -> None:
        value = self.var_erase_statement.get()
        self.save_new_config_handler('apagar_enunciado', value)
        self._var_erase_statement_on_off.set(self.check_state(value))

    def change_auto_exportar(self) -> None:
        value = self.var_auto_export.get()
        self.save_new_config_handler('exportar_automaticamente', value)
        self._var_auto_export_on_off.set(self.check_state(value))

    def salva_e_altera_aparencia(self, value: str) -> None:
        self.save_new_config_handler('aparencia_do_sistema', value)
        self.change_appearance_handler(value)

    def salva_e_altera_escala_do_sistema(self, nova_escala):
        self.save_new_config_handler('escala_do_sistema', nova_escala)
        self.change_scale_handler(nova_escala)

    @staticmethod
    def check_state(state: bool) -> str:
        return 'LIGADO' if state else 'DESLIGADO'
