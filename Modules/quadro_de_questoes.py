from tkinter import Toplevel
from tkinter.ttk import Treeview

from .question import Question


class QuestionFrame:
    def __init__(self, root_configs):
        self.__init__top_level(root_configs)
        self.__init__treeview()
        self.__questions = list()
        self.__question_in_edit = None

    def __init__top_level(self, root_configs):
        question_frame = Toplevel()
        screen_width = question_frame.winfo_screenwidth()
        screen_height = question_frame.winfo_screenheight()
        top_level_width = int(screen_width * 0.5)
        top_level_height = int(screen_height * 0.9)
        question_frame.geometry(f'{top_level_width}x{top_level_height}+{top_level_width}+0')
        question_frame.resizable(False, False)
        question_frame.configure(**root_configs)
        question_frame.title('Tabela de questões criadas')
        question_frame.protocol(question_frame.protocol()[0], self.__disable_event)
        self.__question_frame = question_frame

    def __disable_event(self):
        pass

    def __init__treeview(self):
        self.__tree_view = Treeview(self.__question_frame, selectmode='browse', show='tree headings')

        column_widths = [('Opções', 50), ('Pergunta', 350), ('Tipo', 200), ('Dificuldade', 100)]
        self.__tree_view['columns'] = ['#0'] + [name for name, _ in column_widths]

        for i, (name, width) in enumerate(column_widths):
            self.__tree_view.column('#'+str(i), anchor='w', width=width)
            self.__tree_view.heading('#'+str(i), text=name, anchor='w')

        self.__tree_view.place(relx=0.03, rely=0.02, relheight=0.96, relwidth=0.94)

        self.__tree_view.bind("<Double-1>", self.__double_click)

    def add_question(self, question: Question):
        self.__question_frame.deiconify()
        self.__question_frame.focus_set()
        self.__questions.append(question)
        index = len(self.__questions)

        self.__add_questao_node(question, index)

        pair = index
        for i, (alternative, answer) in enumerate(question.options, start=1):
            index = round(pair + i*0.01, 2)
            self.__add_option_node(alternative, answer, pair, index)

        return pair

    def __add_questao_node(self, question, index):
        self.__tree_view.insert(
            '', 'end', iid=index, text='', values=(question.question, question.type_, question.difficulty)
        )

    def __add_option_node(self, alternative, answer, pair, index):
        self.__tree_view.insert(pair, 'end', iid=index, text='', values=(alternative, answer, ''))

    def __double_click(self, event):
        selection = self.__tree_view.selection()[0]
        if not self.__tree_view.parent(selection):
            index = int(selection) - 1
        else:
            index = int(self.__tree_view.parent(selection)) - 1

        question = self.__questions[index]
        self.__question_in_edit = index
        self.edit_question(question)

    def edited_question(self, question):
        self.__questions[self.__question_in_edit] = question
        item = self.__question_in_edit + 1

        self.__tree_view.set(item, '#1', question.question)
        self.__tree_view.set(item, '#2', question.type_)
        self.__tree_view.set(item, '#3', question.difficulty)

        self.__tree_view.delete(*self.__tree_view.get_children(item))

        pair = item
        for i, (alternative, answer) in enumerate(question.options, start=1):
            index = round(pair + i*0.01, 2)
            self.__add_option_node(alternative, answer, pair, index)
        self.__question_in_edit = None

    def limpa_tree_view(self):
        self.__tree_view.delete(*self.__tree_view.get_children())

    @property
    def get_lista_questoes(self):
        return self.__questions
