from dataclasses import dataclass, field

from src.Constants import CATEGORYLIST, DIFFICULTLIST, QUESTIONTYPELIST
from src.Hints import List


@dataclass(frozen=True)
class UserModel:
    auto_export: bool = field(default=0)
    category_options: List[str] = field(default_factory=list)
    default_font_size: int = field(default=12)
    difficulty_list: List[str] = field(default_factory=list)
    erase_statement: bool = field(default=0)
    font_family: str = field(default='Roboto')
    question_type_list: List[str] = field(default_factory=list)
    title_font_size: int = field(default=15)
    user_appearance_mode: str = field(default='system')
    user_color_theme: str = field(default='green')
    user_default_category: str = field(default='')
    user_scaling: str = field(default='100%')
