from customtkinter import CTk

from front_end import Application
from back_end import API


if __name__ == '__main__':
    main_window = CTk()

    api = API()
    # Application(main_window, api)

    main_window.mainloop()
