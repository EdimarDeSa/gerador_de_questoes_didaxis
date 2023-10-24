from icecream import ic

from model import Model
from ctkview import View


class Controller:
    def __init__(self, views: View, models: Model):
        self.models = models
        self.views = views

        # User settings
        self.titles_font_settings = self.models.titles_font_settings
        self.default_font_settings = self.models.default_font_settings

        self.category_options = self.models.category_options
        self.question_type_list = self.models.question_type_list
        self.difficulty_list = self.models.difficulty_list

        self.setup_bt_img_light = self.models.setup_bt_img_light
        self.setup_bt_img_dark = self.models.setup_bt_img_dark
        self.eraser_light = self.models.eraser_light
        self.eraser_dark = self.models.eraser_dark
        self.edit_light = self.models.edit_light
        self.edit_dark = self.models.edit_dark

    def start(self) -> None:
        self.views.set_appearance(self.models.user_appearance_mode)
        self.views.set_scaling(self.models.user_scaling)
        self.views.set_color_theme(self.models.user_color_theme)
        self.views.setup(self)
        self.views.insert_data_in_question_form(dict(
            categoria='',
            subcategoria='',
            tempo='00:00:00',
            tipo=self.question_type_list[1],
            dificuldade=self.difficulty_list[0],
            peso='1',
        ))

        self.views.start_main_loop()

    def new_bd_handler(self) -> None:
        ...

    def open_bd_handler(self) -> None:
        ...

    def export_bd_handler(self) -> None:
        ...

    def export_as_bd_handler(self) -> None:
        ...

    def save_user_settings_handler(self) -> None:
        ...
