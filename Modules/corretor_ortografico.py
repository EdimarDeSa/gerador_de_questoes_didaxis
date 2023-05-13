from customtkinter import CTkTextbox, CTkButton, CTkScrollableFrame, CTk
from threading import Thread
from tkinter import Menu

from spellchecker.spellchecker import SpellChecker


class SpellCheck(SpellChecker):
    def __init__(self, language: str = 'pt', local_dictionary: str = None):
        SpellChecker.__init__(self, language=language, local_dictionary=local_dictionary, distance=2,
                              case_sensitive=True)


class PowerfullSpellChecker(SpellChecker):
    def __init__(self, text_widget, timeout=5000, max_threads=1, spellcheck_file=None):
        self.__text_widget: CTkTextbox = text_widget
        self.__corrections = {}
        self.__timeout = timeout
        self.__max_threads = max_threads
        self.__timer = None
        self.__running_threads = 0
        self.__checker = SpellCheck(local_dictionary=spellcheck_file)

    def start_timer(self):
        if self.__timer:
            self.__text_widget.after_cancel(self.__timer)
        self.__timer = self.__text_widget.after(self.__timeout, self.__check_spelling)

    def __check_spelling(self):
        if self.__running_threads < self.__max_threads:
            self.__running_threads += 1
            Thread(target=self.__start_thread_check).start()

    def __start_thread_check(self):
        self.__clear_previous_corrections()

        words = self.__checker.split_words(self.__text_widget.get(1.0, "end-1c"))
        for word in words:
            if self.__checker.unknown([word]):
                suggested = self.__checker.candidates(word)
                if suggested:
                    self.__corrections[word] = dict(suggested=list(suggested)[:5] if len(suggested) > 4 else suggested)
                else:
                    self.__corrections[word] = dict(suggested=('Sem sugestões',))

                self.__highlight_word(word)

        self.__running_threads -= 1

    def __highlight_word(self, word):
        start_index = self.__text_widget.search(word, 1.0, 'end')
        end_index = self.__text_widget.search(r'\s|[\.,!?:;\)]', start_index, stopindex='end', regexp=True)
        self.__corrections[word]['start_index'] = start_index
        self.__corrections[word]['end_index'] = end_index
        tag_name = f"spell_check_{start_index}"
        self.__corrections[word]['tag_name'] = tag_name
        self.__text_widget.tag_add(tag_name, start_index, end_index)
        self.__text_widget.tag_config(tag_name, underline=True, underlinefg="red")
        self.__text_widget.tag_bind(tag_name, "<Button-3>", lambda event: self.__show_correction_menu(event, word))

    def __clear_previous_corrections(self):
        for tag_name in self.__text_widget.tag_names():
            if tag_name.startswith("spell_check_"):
                self.__text_widget.tag_delete(tag_name)
                word = tag_name.replace("spell_check_", "")
                self.__corrections.pop(word, None)

    def __show_correction_menu(self, e, word):
        self.pop_up_menu = Menu(self.__text_widget, tearoff=False, font='arial 12')
        for correction in self.__corrections[word]['suggested']:
            self.pop_up_menu.add_command(label=correction, command=lambda correction=correction: self.__apply_correction(correction, word))
        self.pop_up_menu.bind("<Leave>", lambda e: self.hide_correction_menu())
        self.pop_up_menu.tk_popup(x=e.x_root, y=e.y_root, entry=0)

    def __apply_correction(self, correction, word):
        start_index = self.__corrections[word]['start_index']
        end_index = self.__corrections[word]['end_index']
        tag_name = self.__corrections[word]['tag_name']

        self.__text_widget.delete(start_index, end_index)
        self.__text_widget.tag_remove(tag_name, start_index, end_index)
        self.__text_widget.insert(start_index, correction)
        self.__corrections.pop(word)
        self.hide_correction_menu()
        self.__text_widget.focus_set()

    def hide_correction_menu(self):
        self.pop_up_menu.destroy()
