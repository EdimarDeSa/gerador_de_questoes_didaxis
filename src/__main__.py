from controller import Controller
from ctkview import CTkView
from model import Model


def main():
    view = CTkView()
    model = Model()
    controls = Controller(view, model)

    controls.start()

    controls.loop()


if __name__ == '__main__':
    main()
