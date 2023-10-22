from dataclasses import dataclass
from pathlib import Path


@dataclass
class PersonalDictionary:
    dictionary: set | None = None

    @classmethod
    def atualiza_atributo(cls, value: str):
        cls.dictionary.add(value)

    @property
    def to_list(self):
        return list(self.dictionary)

    def __iter__(self):
        return iter(self.__dict__.items())
