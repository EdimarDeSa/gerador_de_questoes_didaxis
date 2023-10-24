from typing import Dict, List, Literal, Callable, Tuple


MenuSettingsHint = Dict[str, ...]

QuestionDataHint = dict[[Literal['categoria'], str],
                        [Literal['subcategoria'], str],
                        [Literal['tempo'], str],
                        [Literal['tipo'], str],
                        [Literal['dificuldade'], str],
                        [Literal['peso'], str],
                        [Literal['pergunta'], str],
                        [Literal['alternativas'], List[Tuple[str, bool]]]]
