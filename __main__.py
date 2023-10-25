from controller import Controller
from ctkview import CTkView
from model import Model


def main():
    views = CTkView()
    models = Model()
    controls = Controller(views, models)

    controls.start()


if __name__ == '__main__':
    main()
