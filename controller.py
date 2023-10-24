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
        self.user_color_theme = self.models.user_color_theme
        self.user_scaling = self.models.user_scaling
        self.user_appearance_mode = self.models.user_appearance_mode

        self.category_options = self.models.category_options
        self.question_type_list = self.models.question_type_list
        self.difficulty_list = self.models.difficulty_list

    def start(self):
        self.views.setup(self)
        self.views.start_main_loop()
