from dataclasses import dataclass, field

from src.Hints import List


@dataclass(frozen=True)
class UserModel:
    auto_export: bool = False
    category_options: List[str] = field(default_factory=list)
    default_font_size: int = 12
    difficulty_list: List[str] = field(default_factory=list)
    erase_statement: bool = False
    font_family: str = 'Roboto'
    question_type_list: List[str] = field(default_factory=list)
    title_font_size: int = 15
    user_appearance_mode: str = 'system'
    user_color_theme: str = 'green'
    user_default_category: str = ''
    user_scaling: str = '100%'
