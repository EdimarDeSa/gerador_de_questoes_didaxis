# from ..Hints import

from customtkinter import IntVar, StringVar, BooleanVar

from ..caixa_de_texto import CaixaDeTexto
from typing import Callable, ClassVar, Optional, Dict, List, LiteralString, Literal, TypeVar


T = TypeVar('T')


# Configs hints
LabelConfigs = ListConfigs = ButtonConfigs = EntryConfigs = SubcategoryVar = TimeVar = ClassVar[Dict]


# Callable hints
TypeChangeHandler = Callable[[T], None]
AddChoiceHandler = Callable[[Optional[str], Optional[int]], None]
RmChoiceHandler = Callable[[Optional[int]], None]
StartMonitorHandler = Callable[[CaixaDeTexto], None]

# ClassVar hints
DisplayQuestionCount = ClassVar[IntVar]
CategoryVar = ClassVar[StringVar]
CategoryList = ClassVar[List]
TypeVar = ClassVar[StringVar]
TypeList = ClassVar[List]
DifficultiesList = ClassVar[List]
DifficultVar = ClassVar[StringVar]
WeightVar = ClassVar[StringVar]

