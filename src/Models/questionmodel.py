from dataclasses import dataclass, field


@dataclass
class QuestionModel:
    id: str
    tipo: str
    peso: int
    tempo: str
    controle: int
    pergunta: str
    categoria: str
    subcategoria: str
    dificuldade: str
    alternativas: list = field(default_factory=list)

    def __iter__(self) -> iter:
        return iter(self.__dict__.values())

    def update(self, **kwargs) -> None:
        self.__dict__.update(**kwargs)
