from dataclasses import dataclass, field

from Modules.constants import D, ME, MEN, VF, CORRETA, V, F


@dataclass
class ModeloQuestao:
    id: int | None
    tipo: str | None
    peso: str | None
    tempo: str | None
    controle: int | None
    pergunta: str | None
    categoria: str | None
    subcategoria: str | None
    dificuldade: str | None
    alternativas: list[tuple[str, bool]] | None = field(default_factory=list)
