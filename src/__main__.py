from controller import Controller
from ctkview import CTkView
from model import Model


def main():
    controls = Controller(CTkView(), Model())

    controls.start()

    controls.loop()


if __name__ == '__main__':
    main()
