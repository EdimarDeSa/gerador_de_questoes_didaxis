from typing import Literal, Callable, Optional, Type

from customtkinter import CTkFrame

RowHint = dict[int, dict[[Literal['row'], CTkFrame], [Literal['display'], object]]]
