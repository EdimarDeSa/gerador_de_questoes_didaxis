from pathlib import Path
import tempfile

from .FileManagerLib import AbrirArquivo, JsonSerializer, BinarySerializer


class FileManager:
    def __init__(self):
        self.base_dir = Path().resolve()

        self.loaded_file: Path = AbrirArquivo.get_desktop_path()

        self._temp_dir = tempfile.gettempdir()

    @staticmethod
    def read_json(path: Path) -> dict | list:
        return JsonSerializer.read_json(path)

    @staticmethod
    def save_json(path: Path, data: dict | list) -> None:
        JsonSerializer.save_json(path, data)

    @staticmethod
    def read_bin(path: Path) -> str:
        return BinarySerializer.read_bin(path)

    @staticmethod
    def save_bin(path: Path, data: str) -> None:
        BinarySerializer.save_bin(path, data)

    def create_personal_dict(self, source_path: Path, dest_path: Path) -> bool:
        if not source_path.exists():
            raise FileExistsError(f'{source_path} does not exist!')
        unserialized_dictionary = self.read_bin(source_path)
        self.save_json(dest_path, unserialized_dictionary.split('\n'))
        return True

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
    def open_db(self, path: Path):
        pass
