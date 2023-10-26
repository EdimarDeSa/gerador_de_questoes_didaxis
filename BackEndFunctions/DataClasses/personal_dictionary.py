from dataclasses import dataclass, field
from typing import Iterator, Optional, List


class PersonalDictionary:
    def __init__(self, words_set):
        self.words_set: set[str] = set(words_set)

    def atualiza_atributo(self, value: str) -> None:
        self.words_set.add(value)

    @property
    def to_list(self) -> List:
        return list(self)

    def __iter__(self) -> Iterator:
        return iter(self.__dict__.items())
