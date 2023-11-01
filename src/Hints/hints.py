from tkinter import Variable
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Literal,
    Optional,
    Tuple,
)

from PIL import Image
from typing_extensions import Protocol, TypedDict


class QuestionDataHint(TypedDict):
    id: Optional[str]
    categoria: str
    subcategoria: Optional[str]
    controle: Optional[int]
    tempo: Optional[str]
    tipo: str
    dificuldade: str
    peso: int
    pergunta: str
    alternativas: List[Tuple[str, bool]]


QuestionsDBHint = Dict[int, QuestionDataHint]


class QuestionDBHint(TypedDict):
    id: Optional[str]
    categoria: str
    subcategoria: Optional[str]
    controle: Optional[int]
    tempo: Optional[str]
    tipo: str
    dificuldade: str
    peso: int
    pergunta: str
    alternativa: Optional[str]
    correta: Optional[str]


ListDBHint = List[QuestionDBHint]
GroupedQuestionDBHint = Dict[str, ListDBHint]


class FontHint(TypedDict):
    font_family: str
    font_size: int
    font_weight: int
    font: Tuple[str, int]


class UserSetHint(TypedDict):
    auto_export: bool
    category_options: str
    default_font_size: int
    difficulty_list: list
    erase_statement: bool
    font_family: str
    question_type_list: list
    title_font_size: int
    user_appearance_mode: str
    user_color_theme: str
    user_default_category: str
    user_scaling: str


class ImageModelHint(TypedDict):
    configuracoes_light_mode: str
    configuracoes_dark_mode: str
    eraser_light_mode: str
    eraser_dark_mode: str
    edit_light_mode: str
    edit_dark_mode: str


class SysImgHint(TypedDict):
    configuracoes_light_mode: Image.Image
    configuracoes_dark_mode: Image.Image
    eraser_light_mode: Image.Image
    eraser_dark_mode: Image.Image
    edit_light_mode: Image.Image
    edit_dark_mode: Image.Image


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
