from customtkinter import CTk

from front_end import Application
from back_end import API


if __name__ == '__main__':
    main_window = CTk()

    largura, altura = 1500, 750
    pos_x = (main_window.winfo_screenwidth() - largura) // 2
    pos_y = (main_window.winfo_screenheight() - altura) // 2 - 35
    main_window.geometry(f'{largura}x{altura}+{pos_x}+{pos_y}')
    main_window.resizable(False, False)

    api = API(main_window)
    Application(main_window, api)

    main_window.mainloop()
