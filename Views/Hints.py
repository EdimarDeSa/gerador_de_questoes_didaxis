from typing import Dict, List, Literal, Callable, Tuple, Optional

from PIL import Image


MenuSettingsHint = Dict[str, ...]

QuestionDataHint = dict[[Literal['categoria'], str],
                        [Literal['subcategoria'], str],
                        [Literal['tempo'], str],
                        [Literal['tipo'], str],
                        [Literal['dificuldade'], str],
                        [Literal['peso'], str],
                        [Literal['pergunta'], str],
                        [Literal['alternativas'], List[Tuple[str, bool]]]]

ChoicesHints = List[Tuple[str, bool]]

WidgetListHint = List

SysImgHint = dict[[Literal['configuracoes_light_mode'], Image],
                  [Literal['configuracoes_dark_mode'], Image],
                  [Literal['eraser_light_mode'], Image],
                  [Literal['eraser_dark_mode'], Image],
                  [Literal['edit_light_mode'], Image],
                  [Literal['edit_dark_mode'], Image],]

UserSetHint = dict[[Literal['titles_font_settings'], str],
                   [Literal['default_font_settings'], str],
                   [Literal['user_appearance_mode'], str],
                   [Literal['user_scaling'], str],
                   [Literal['erase_statement'], str],
                   [Literal['user_color_theme'], str],
                   [Literal['auto_export'], str]]

