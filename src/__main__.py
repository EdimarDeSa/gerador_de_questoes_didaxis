from controller import Controller
from ctkview import CTkView
from model import Model


def main():
    model = Model()
    view = CTkView()
    controls = Controller()

    controls.start(view, model)

    controls.loop()


if __name__ == "__main__":
    main()
