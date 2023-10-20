from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from ..funcoes import FileSerializer


__all__ = ['Configuracoes']


@dataclass
class Configuracoes:
    fonte: str = 'Arial'
    tamanho_texto: int = 8
    tamanho_titulo: int = 10
    fonte_estilo: Literal['bold', 'normal'] = 'bold'
    tipos: list[str] = field(default_factory=lambda: [
        'Multipla escolha 1 correta', 'Multipla escolha n corretas', 'Verdadeiro ou falso'
    ])
    unidades: list[str] = field(default_factory=lambda: [
        'Astec', 'Comunicação', 'Controle de acesso', 'Energia', 'Exportação', 'Gestão', 'Incêndio e iluminação',
        'Negócios', 'Redes', 'Segurança eletrônica', 'Solar', 'Soluções', 'Varejo', 'Verticais'
    ])
    dificuldades: list[str] = field(default_factory=lambda: ['Fácil', 'Médio', 'Difícil'])

    def atualiza_atributo(self, *, path: Path, key: str, value: any):
        setattr(self, key, value)
        FileSerializer.save_json(path, self.__dict__)

