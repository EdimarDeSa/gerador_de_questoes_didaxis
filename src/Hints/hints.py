from tkinter import Variable
from typing import Dict, List, Callable, Tuple, Optional, Any, Literal

from typing_extensions import TypedDict, Protocol


class QuestionDataHint(TypedDict):
    categoria: str
    subcategoria: str
    tempo: str
    tipo: str
    dificuldade: str
    peso: int
    pergunta: str
    alternativas: List[Tuple[str, bool]]


class FontHint(TypedDict):
    font_family: str
    font_size: int
    font_weight: int
    font: Tuple[str, int]


class UserSetHint(TypedDict):
    titles_font_settings: FontHint
    default_font_settings: FontHint
    user_appearance_mode: str
    user_scaling: str
    user_color_theme: str
    erase_statement: bool
    auto_export: bool
    user_default_category: str
    category_options: str
    question_type_list: str
    difficulty_list: str


class SysImgHint(TypedDict):
    configuracoes_light_mode: Optional[None]
    configuracoes_dark_mode: Optional[None]
    eraser_light_mode: Optional[None]
    eraser_dark_mode: Optional[None]
    edit_light_mode: Optional[None]
    edit_dark_mode: Optional[None]


class RowFrame(Protocol):
    def destroy(self):
        ...

    def configure(self, **kwargs):
        ...


class QuestionLineHint(TypedDict):
    row: RowFrame
    display: Variable


class TkVariable(Protocol):
    def get(self):
        ...

    def set(self):
        ...


RowDict = Dict[int, QuestionLineHint]


ChoicesHint = List[Optional[Tuple[str, bool]]]

WidgetListHint = List[Any]

MenuSettingsHint = Dict[str, Any]
