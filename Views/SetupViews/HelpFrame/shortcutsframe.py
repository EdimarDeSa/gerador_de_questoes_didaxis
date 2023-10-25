from customtkinter import CTkScrollableFrame, CTkLabel, E, W

from Views.Hints import MenuSettingsHint


# TODO: Variável posta


SHORTCUTS = [
    ('Abre tela de atalhos:', 'F1'),
    ('Salvar como:', 'F12'),
    ('Salva questão:', 'Ctrl + S'),
    ('Abrir:', 'Ctrl + O'),
    ('Exportar:', 'Ctrl + E'),
    ('Adiciona opção:', 'Ctrl + "+" ou Ctrl + "="'),
    ('Remover opção:', 'Ctrl + "-"'),
    ('Alterar tipo da questão:', 'Ctrl + 1, 2 ou 3'),
    ('Alterar dificuldade:', 'Ctrl + 4, 5 ou 6'),
    ('Desfazer:', 'Ctrl + Z'),
    ('Refazer:', 'Ctrl + Y'),
    ('Pular campos:', 'Ctrl + TAB ou TAB'),
    ('Voltar campos:', 'Ctrl + Shift + TAB ou Shift + TAB')
]


class ShortcutsFrame(CTkScrollableFrame):
    def __init__(self, master, label_settings: MenuSettingsHint, **kwargs):
        super().__init__(master, **kwargs)

        for i in range(2): self.grid_columnconfigure(i, weight=i+1)

        pad = dict(padx=2, pady=5)

        for i, (descricao, atalho) in enumerate(SHORTCUTS):
            CTkLabel(self, text=descricao, **label_settings).grid(column=0, row=i, sticky=E, **pad)
            CTkLabel(self, text=atalho, **label_settings).grid(column=1, row=i, sticky=W, **pad)
