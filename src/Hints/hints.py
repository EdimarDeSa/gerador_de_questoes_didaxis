from threading import Timer
from typing import Any, Callable, Dict, Iterable, List, Literal, Optional, Tuple

from PIL import Image
from typing_extensions import Protocol, TypedDict, ClassVar

from ..Contracts.spelledtextbox import SpelledTextBoxContract


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


class ImageType:
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, Image.Image):
            raise ValueError('Deve ser uma instância de PIL.Image.Image')
        return v

#
# class SysImgHint(TypedDict):
#     configuracoes_light_mode: ImageType
#     configuracoes_dark_mode: ImageType
#     eraser_light_mode: ImageType
#     eraser_dark_mode: ImageType
#     edit_light_mode: ImageType
#     edit_dark_mode: ImageType


class RowFrame(Protocol):
    def destroy(self):
        ...

    def configure(self, **kwargs):
        ...


class TkVariable(Protocol):
    def get(self):
        ...

    def set(self):
        ...


class QuestionLineHint(TypedDict):
    row: RowFrame
    display: TkVariable


RowDict = Dict[int, QuestionLineHint]


ChoicesHint = List[Optional[Tuple[str, bool]]]

WidgetListHint = List[Any]

MenuSettingsHint = Dict[str, Any]


class WidgetInfosHint(TypedDict):
    widget: SpelledTextBoxContract
    timer: Timer
    words: List[str]
