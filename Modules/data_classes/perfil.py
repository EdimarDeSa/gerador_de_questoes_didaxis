from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from ..funcoes import FileSerializer


__all__ = ['Perfil']


@dataclass
class Perfil:
    unidade_padrao: str = ''
    apagar_enunciado: bool = False
    aparencia_do_sistema: Literal['system', 'dark', 'light'] = 'System'
    escala_do_sistema: str = '100%'
    cor_padrao: str = 'green'

    def atualiza_atributo(self, *, path: Path, key: str, value: any):
        setattr(self, key, value)
        FileSerializer.save_json(path, self.__dict__)
