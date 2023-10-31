from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from src.Constants import EASY


@dataclass(frozen=True)
class QuestionModel:
    id: Optional[str] = field(default=None, compare=False)
    tipo: str = field(default='', compare=False)
    peso: int = field(default=1, compare=False)
    tempo: str = field(default='00:00:00', compare=False)
    controle: Optional[int] = field(default=None, compare=False)
    pergunta: str = field(default='')
    categoria: str = field(default='', compare=False)
    subcategoria: Optional[str] = field(default=None, compare=False)
    alternativas: List[Tuple[str, bool]] = field(
        default_factory=list, compare=False
    )
    dificuldade: str = field(default=EASY, compare=False)
