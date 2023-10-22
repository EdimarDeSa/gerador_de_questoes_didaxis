from dataclasses import dataclass, field
from typing import Optional


@dataclass
class QuestionDataClass:
    id: Optional[int] = field(default=None, compare=False)
    tipo: Optional[str] = field(default=None, compare=False)
    peso: Optional[str] = field(default=None, compare=False)
    tempo: Optional[str] = field(default=None, compare=False)
    controle: Optional[int] = field(default=None, compare=False, init=False)
    pergunta: Optional[str] = field(default=None)
    categoria: Optional[str] = field(default=None, compare=False)
    subcategoria: Optional[str] = field(default=None, compare=False)
    alternativas: Optional[list[tuple[str, bool]]] = field(default_factory=list, compare=False)
    dificuldade: Optional[str] = field(default=None, compare=False)

    def __iter__(self) -> iter:
        return iter(self.__dict__.items())