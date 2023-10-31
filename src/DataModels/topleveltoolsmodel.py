from dataclasses import dataclass

from src.Hints import Callable, Variable


@dataclass(frozen=True)
class TopLevelToolsModel:
    new_db: Callable[[], None]
    open_db: Callable[[], None]
    export_db: Callable[[], None]
    set_appearance: Callable[[], None]
    set_scaling: Callable[[], None]
    category: Variable
    var_erase_statement: Variable
    var_auto_export: Variable
