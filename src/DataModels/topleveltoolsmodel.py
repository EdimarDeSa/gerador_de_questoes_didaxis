from dataclasses import dataclass

from ..Hints import Callable, TkVariable


@dataclass
class TopLevelToolsModel:
    new_db: Callable[[], None]
    open_db: Callable[[], None]
    export_db: Callable[[], None]
    set_appearance: Callable[[], None]
    set_scaling: Callable[[], None]
    category: TkVariable
    var_erase_statement: TkVariable
    var_auto_export: TkVariable
