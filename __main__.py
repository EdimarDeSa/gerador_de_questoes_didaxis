from src.controller import Controller
from src.ctkview import CTkView
from src.model import Model


def main():
    model = Model()
    view = CTkView()
    controls = Controller()

    controls.start(view, model)

    controls.loop()


if __name__ == '__main__':
    main()
