from pathlib import Path
import tempfile

from .FileManagerLib import save_json, read_json, save_bin, read_bin


class FileManager:
    def __init__(self):
        self.base_dir = Path().resolve()

        self.loaded_file: Path | None = None

        self._temp_dir = tempfile.gettempdir()

    @staticmethod
    def read_json(path: Path) -> dict | list:
        return read_json(path)

    @staticmethod
    def save_json(path: Path, data: dict | list) -> bool:
        return save_json(path, data)

    @staticmethod
    def read_bin(path: Path) -> str:
        return read_bin(path)

    @staticmethod
    def save_bin(path: Path, data: str) -> bool:
        return save_bin(path, data)

    def create_personal_dict(self, source_path: Path, dest_path: Path) -> bool:
        if not source_path.exists():
            raise FileExistsError(f'{source_path} does not exist!')
        unserialized_dictionary = self.read_bin(source_path)
        self.save_json(dest_path, unserialized_dictionary.split('\n'))
        return True

    # @staticmethod
    # def _open_save_dir() -> Path | None:
    #     caminho = asksaveasfilename(
    #         confirmoverwrite=True, defaultextension=EXTENSIONS, filetypes=FILETYPES, initialfile='novo_banco',
    #         initialdir=AbrirArquivo.get_desktop_path(),
    #     )
    #     if not caminho:
    #         return None
    #
    #     return Path(caminho).resolve()
    #
    # def exportar(self, lista_serial: list[dict]) -> bool | None:
    #     if self.dir_atual is None:
    #         caminho = self._open_save_dir()
    #         if caminho is None:
    #             return None
    #         self.dir_atual = self._open_save_dir()
    #
    #     salvo = SalvarArquivo(lista_serial=lista_serial, path=self.dir_atual)
    #
    #     if not salvo:
    #         return False
    #     return True
