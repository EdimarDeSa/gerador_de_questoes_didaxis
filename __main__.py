# from customtkinter import CTk
#
# from front_end import Application
# from back_end import Controller
#
#
# if __name__ == '__main__':
#
#     main_window = CTk()
#
#     largura, altura = 1500, 750
#     pos_x = (main_window.winfo_screenwidth() - largura) // 2
#     pos_y = (main_window.winfo_screenheight() - altura) // 2 - 35
#     main_window.geometry(f'{largura}x{altura}+{pos_x}+{pos_y}')
#     main_window.resizable(False, False)
#     main_window.wm_iconbitmap(default='./icons/prova.ico')
#
#     api = Controller(main_window)
#     Application(main_window, api)
#
#     main_window.mainloop()


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
