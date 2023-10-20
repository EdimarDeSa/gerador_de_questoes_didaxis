from dataclasses import dataclass, field


__all__ = ['ModeloQuestao']


@dataclass
class ModeloQuestao:
    id: int | None = field(default=None)
    tipo: str | None = field(default=None)
    peso: str | None = field(default=None)
    tempo: str | None = field(default=None)
    controle: int | None = field(default=None)
    pergunta: str | None = field(default=None)
    categoria: str | None = field(default=None)
    subcategoria: str | None = field(default=None)
    alternativas: list[tuple[str, bool]] | None = field(default_factory=list)
    dificuldade: str | None = field(default=None)
