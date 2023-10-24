from icecream import ic

from model import Model
from ctkview import View


class Controller:
    def __init__(self, views: View, models: Model):
        self.models = models
        self.views = views

    def start(self):
        self.views.setup(self)
        self.views.start_main_loop()
