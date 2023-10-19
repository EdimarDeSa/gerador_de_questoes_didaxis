from pathlib import Path
from tkinter.filedialog import asksaveasfilename

from pandas import DataFrame, ExcelWriter

from ..constants import CABECALHO_DIDAXIS_LOWER, ERRADA, CORRETA, F, V, EXTENSIONS, FILETYPES, CABECALHO_DIDAXIS, ENGINE


__all__ = ['SalvarArquivo']


class SalvarArquivo:
    _success = False

    def __init__(self, *, lista_serial: list[dict], path: Path):
        self.save_file(lista_serial, path)

    @staticmethod
    def _verify_keys(serial_keys: dict.keys) -> bool:
        return set(serial_keys) == set(CABECALHO_DIDAXIS_LOWER)

    @staticmethod
    def _normalize_keys(to_normalize: dict) -> dict:
        """
        Normaliza as chaves do dicionário para letras minúsculas.

        Normalizes dictionary keys to lowercase.

        :param to_normalize: Um dicionário a ser normalizado.
        :return: Um dicionário com chaves em letras minúsculas.
        """
        return {key.upper(): value for key, value in to_normalize.items()}

    @staticmethod
    def _converte_correta(correct: bool, _type: str) -> None | str:
        """
        Converte o valor da resposta correta de acordo com o tipo de questão.

        Convert the value of the correct answer based on the question type.
        """
        tipo_para_correto = {
            'me': (ERRADA, CORRETA),
            'men': (ERRADA, CORRETA),
            'vf': (F, V),
            'd': (ERRADA, ERRADA)
        }
        return tipo_para_correto.get(_type)[int(correct)]

    @classmethod
    def _normalize_serials(cls, lista_serial: list[dict]) -> list[dict]:
        """
        Normaliza as entradas da lista de questões serializadas.

        Normalize the entries in the list of serialized questions.
        """
        new_serialized_list = []
        for serial in lista_serial:
            choices = serial.get('alternativas')
            _type = serial.get('tipo')
            del serial['alternativas']
            for choice, correct in choices:
                resultado = dict(alternativa=choice, correta=cls._converte_correta(correct, _type))
                new_serial = serial.copy()  # Create a new copy of the 'serial' dictionary
                new_serial.update(resultado)
                new_serial = cls._normalize_keys(new_serial)
                new_serialized_list.append(new_serial)

        return new_serialized_list

    @classmethod
    def save_file(cls, lista_serial: list[dict], path: Path):
        for serial in lista_serial:

            if not cls._verify_keys(serial.keys()):
                raise KeyError(f'Os dicionários devem conter as chaves: {CABECALHO_DIDAXIS_LOWER}')

        normalized_path = Path(path).resolve()

        normalized_lista_serial = cls._normalize_serials(lista_serial)

        data_frame = DataFrame(normalized_lista_serial, columns=CABECALHO_DIDAXIS)
        try:
            with ExcelWriter(normalized_path, engine=ENGINE) as writer:
                data_frame.to_excel(writer, index=False)
        except PermissionError as err:
            raise PermissionError(err)
        cls._success = True

    def __bool__(self):
        return self._success
