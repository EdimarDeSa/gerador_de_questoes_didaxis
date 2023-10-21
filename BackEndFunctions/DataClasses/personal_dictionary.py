from dataclasses import dataclass
from pathlib import Path


@dataclass
class PersonalDictionary:
    dictionary: set | None = None

    @classmethod
    def atualiza_atributo(cls, value: str):
        cls.dictionary.add(value)

    @property
    def __list__(self):
        return list(self.dictionary)
