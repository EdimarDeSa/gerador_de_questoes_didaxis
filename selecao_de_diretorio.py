from tkinter.filedialog import askopenfilename, asksaveasfilename
from os.path import abspath


class SelecionaPasta:
    __abre_fecha_params = dict(filetypes = [('banco em xlsx', '*.xlsx')], initialdir = './')

    @classmethod
    def abrir_arquivo(cls):
        file = askopenfilename(**cls.__abre_fecha_params)
        return abspath(file)

    @classmethod
    def salvar_como(cls):
        file = asksaveasfilename(**cls.__abre_fecha_params)
        extensao = '.xlsx'
        if file[-5:] != extensao:
            file += extensao
        print(file)
        return abspath(file)
