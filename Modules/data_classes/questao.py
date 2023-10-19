from dataclasses import dataclass, field


__all__ = ['ModeloQuestao']


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
