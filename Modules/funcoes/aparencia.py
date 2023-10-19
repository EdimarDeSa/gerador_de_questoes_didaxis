from customtkinter import set_appearance_mode, set_widget_scaling, set_window_scaling, set_default_color_theme
from typing import Literal


__all__ = ['altera_aparencia', 'altera_escala', 'altera_cor_padrao']


def altera_aparencia(config: Literal['system', 'dark', 'light']):
    set_appearance_mode(config)


def altera_escala(config: str):
    nova_escala_float = int(config.replace("%", "")) / 100
    set_widget_scaling(nova_escala_float)
    set_window_scaling(nova_escala_float)


def altera_cor_padrao(config: str):
    set_default_color_theme(config)
