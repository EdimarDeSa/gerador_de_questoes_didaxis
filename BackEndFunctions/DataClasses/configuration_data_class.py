from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from ..Constants import FONTFAMILY, UNIDADES, TYPESLIST, SUBCATEGORYLIST


@dataclass
class ConfigurationDataClass:
    fonte: str = field(default=FONTFAMILY, compare=True)
    tamanho_texto: int = field(default=12, compare=True)
    tamanho_titulo: int = field(default=15, compare=True)
    fonte_estilo: Literal['bold', 'normal'] = field(default='bold', compare=True)

    tipos: list[str] = field(default_factory=lambda: TYPESLIST, compare=True)
    unidades: list[str] = field(default_factory=lambda: UNIDADES, compare=True)
    dificuldades: list[str] = field(default_factory=lambda: SUBCATEGORYLIST, compare=True)

    def atualiza_atributo(self, key: str, value: any):
        setattr(self, key, value)
