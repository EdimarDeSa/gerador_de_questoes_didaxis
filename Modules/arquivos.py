from pathlib import Path
import tempfile
from tkinter.filedialog import asksaveasfilename

from Modules.constants import EXTENSIONS, FILETYPES
from Modules.funcoes import AbrirArquivo, SalvarArquivo, FileSerializer


class Arquivos:
    def __init__(self):
        self._temp_dir = tempfile.gettempdir()
        self.dir_atual: Path | None = None
        self.base_dir = Path(__file__).resolve().parent.parent

    def cria_dicionario_pessoal(self, path: Path):
        unserialized_dictionary = FileSerializer.abre_bin(self.base_dir / './configs/lista_de_paralvras.bin')
        FileSerializer.save_json(path, unserialized_dictionary)

    @staticmethod
    def _open_save_dir() -> Path | None:
        caminho = asksaveasfilename(
            confirmoverwrite=True, defaultextension=EXTENSIONS, filetypes=FILETYPES, initialfile='novo_banco',
            initialdir=AbrirArquivo.get_desktop_path(),
        )
        if not caminho:
            return None

        return Path(caminho).resolve()

    def exportar(self, lista_serial: list[dict]) -> bool | None:
        if self.dir_atual is None:
            caminho = self._open_save_dir()
            if caminho is None:
                return None
            self.dir_atual = self._open_save_dir()

        salvo = SalvarArquivo(lista_serial=lista_serial, path=self.dir_atual)

        if not salvo:
            return False
        return True
