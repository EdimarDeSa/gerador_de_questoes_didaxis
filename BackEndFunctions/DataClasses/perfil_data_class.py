from typing import Iterator, Any
from dataclasses import dataclass, field


@dataclass
class PerfilDataClass:
    unidade_padrao: str = field(default='', compare=True)
    apagar_enunciado: bool = field(default=False, compare=True)
    aparencia_do_sistema: str = field(default='system', compare=True)
    escala_do_sistema: str = field(default='100%', compare=True)
    cor_padrao: str = field(default='green', compare=True)
    exportar_automaticamente: bool = field(default=False, compare=True)

    def atualiza_atributo(self, key: str, value: Any) -> None:
        setattr(self, key, value)

    def __iter__(self) -> Iterator:
        return iter(self.__dict__.items())
