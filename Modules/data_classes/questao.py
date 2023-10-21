from dataclasses import dataclass, field


__all__ = ['ModeloQuestao']


@dataclass
class ModeloQuestao:
    id: int | None = field(default=None, compare=False)
    tipo: str | None = field(default=None, compare=False)
    peso: str | None = field(default=None, compare=False)
    tempo: str | None = field(default=None, compare=False)
    controle: int | None = field(default=None, compare=False)
    pergunta: str | None = field(default=None)
    categoria: str | None = field(default=None, compare=False)
    subcategoria: str | None = field(default=None, compare=False)
    alternativas: list[tuple[str, bool]] | None = field(default_factory=list, compare=False)
    dificuldade: str | None = field(default=None, compare=False)
