from dataclasses import dataclass, field

from src.Constants import CATEGORYLIST, DIFFICULTLIST, QUESTIONTYPELIST


@dataclass
class UserModel:
    auto_export: bool = field(default=0)
    category_options: list = field(default_factory=list)
    default_font_size: int = field(default=12)
    difficulty_list: list = field(default_factory=list)
    erase_statement: bool = field(default=0)
    font_family: str = field(default="Roboto")
    question_type_list: list = field(default_factory=list)
    title_font_size: int = field(default=15)
    user_appearance_mode: str = field(default="system")
    user_color_theme: str = field(default="green")
    user_default_category: str = field(default="")
    user_scaling: str = field(default="100%")

    def __post_init__(self):
        if not self.category_options:
            self.category_options = CATEGORYLIST
        if not self.question_type_list:
            self.question_type_list = QUESTIONTYPELIST
        if not self.difficulty_list:
            self.difficulty_list = DIFFICULTLIST

    def __iter__(self):
        return iter(self.__dict__.items())

    def updatesetting(self, attribute: str, value: any) -> None:
        setattr(self, attribute, value)
