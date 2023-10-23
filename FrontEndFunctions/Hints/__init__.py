from typing import Callable, ClassVar, Optional, Dict, List, TypeVar, Literal

from customtkinter import IntVar, StringVar, BooleanVar, CTkImage, CTkFrame

from ..caixa_de_texto import CaixaDeTexto


T = TypeVar('T')


# Configs hints
ConfigsHint = ClassVar[Dict[str, any]]
ImageHint = ClassVar[CTkImage]


# Callable hints
TypeChangeHandler = Callable[[T], None]
AddChoiceHandler = Callable[[Optional[str], Optional[int]], None]
RmChoiceHandler = Callable[[Optional[int]], None]
StartMonitorHandler = Callable[[CaixaDeTexto], None]
OpenDbHandler = ShowWindowHandler = ExportHandler = SaveQuestionHandler = Callable[[T], None]
SaveNewConfigHint = Callable[[str, any], None]


# ClassVar hints
CategoryList = ClassVar[List[str]]
TypeList = ClassVar[List[str]]
DifficultiesList = ClassVar[List[str]]
ListHint = ClassVar[List]

IntVarHint = ClassVar[IntVar]
StringVarHint = ClassVar[StringVar]
BooleanVarHint = ClassVar[BooleanVar]

