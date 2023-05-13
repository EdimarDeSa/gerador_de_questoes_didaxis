
from customtkinter import CTkEntry


class PlaceHolderEntry(CTkEntry):
    def __init__(self, master=None, placeholder="Texto padrão", color='gray30', **kw):
        super().__init__(master, kw)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

        self.set_placeholder()

    def set_placeholder(self):
        self.insert(0, self.placeholder)
        self.configure(fg=self.placeholder_color)

    def on_focus_in(self, event):
        if self['fg'] == self.placeholder_color:
            self.delete(0, 'end')
            self['fg'] = self.default_fg_color

    def on_focus_out(self, event):
        if not self.get():
            self.set_placeholder()
