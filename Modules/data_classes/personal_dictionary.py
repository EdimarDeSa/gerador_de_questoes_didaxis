from dataclasses import dataclass
from pathlib import Path

from ..funcoes import FileSerializer


__all__ = ['PersonalDictionary']


@dataclass
class PersonalDictionary:
    dictionary: set | None = None

    def atualiza_atributo(self, path: Path, value: any):
        self.dictionary.add(value)
        FileSerializer.save_json(path, list(self.dictionary))
