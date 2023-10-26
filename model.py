from icecream import ic


# Unidades de negócio
ASTEC = 'Astec'
COMUNICACAO = 'Comunicação'
CONTROLE = 'Controle de acesso'
ENERGIA = 'Energia'
EXPORTACAO = 'Exportação'
GESTAO = 'Gestão'
INCENDIO = 'Incêndio e iluminação'
NEGOCIOS = 'Negócios'
REDES = 'Redes'
SEGURANCA = 'Segurança eletrônica'
SOLAR = 'Solar'
SOLUCOES = 'Soluções'
VAREJO = 'Varejo'
VERTICAIS = 'Verticais'
CATEGORYLIST = [ASTEC, COMUNICACAO, CONTROLE, ENERGIA, EXPORTACAO, GESTAO, INCENDIO,
                NEGOCIOS, REDES, SEGURANCA, SOLAR, SOLUCOES, VAREJO, VERTICAIS]

# Constantes para tipos de questão
D = 'Dissertativa'
ME = 'Multipla escolha 1 correta'
MEN = 'Multipla escolha n corretas'
VF = 'Verdadeiro ou falso'
TYPELIST = [D, ME, MEN, VF]

# Subcategorias
FACIL = 'Fácil'
MEDIO = 'Médio'
DIFICIL = 'Difícil'
DIFFICULTLIST = [FACIL, MEDIO, DIFICIL]


# Theme settings
COLORTHEMELIST = ['dark-blue', 'blue', 'green']
SCALESTHEMELIST = ['80%', '90%', '100%', '110%', '120%', '130%', '140%', '150%']
APPEARANCEMODETHEME = ["Light", "Dark", "System"]

from pathlib import Path
from PIL import Image
from dataclasses import dataclass, field
from typing import Dict


@dataclass(kw_only=True)
class ImageManager:
    icons_dir: Path
    image_paths: Dict[str, str]

    def __post_init__(self):
        self._images = {name: self._abre_imagem(path) for name, path in self.image_paths.items()}

    def _abre_imagem(self, nome_imagem: str) -> Image:
        caminho_imagem = self.icons_dir / nome_imagem
        return Image.open(caminho_imagem)

    def get_images(self) -> Dict[str, Image]:
        return self._images


@dataclass
class UserManager:
    erase_statement: bool = False
    auto_export: bool = False
    user_default_category: str = field(default='')
    user_color_theme: str = field(default='green')
    user_scaling: str = field(default='100%')
    user_appearance_mode: str = field(default='system')
    titles_font_settings: dict = field(default_factory=dict)
    default_font_settings: dict = field(default_factory=dict)
    category_options: list = field(default_factory=list)
    question_type_list: list = field(default_factory=list)
    difficulty_list: list = field(default_factory=list)

    def __iter__(self):
        return iter(self.__dict__.items())

    def updatesetting(self, attribute: str, value: any) -> None:
        setattr(self, attribute, value)


class Model:
    def __init__(self):
        local = Path().resolve()

        icons_dir = local / 'icons'
        self._img_manager = ImageManager(icons_dir=icons_dir, image_paths={
                'configuracoes_light_mode': 'configuracoes_light_mode.png',
                'configuracoes_dark_mode': 'configuracoes_dark_mode.png',
                'eraser_light_mode': 'eraser_light_mode.png',
                'eraser_dark_mode': 'eraser_dark_mode.png',
                'edit_light_mode': 'edit_light_mode.png',
                'edit_dark_mode': 'edit_dark_mode.png',
            })
        self.system_images: Dict[str, Image] = self._img_manager.get_images()

        configs_dir = local / 'configs'
        self._user_manager = UserManager(
            titles_font_settings={'font': ('Roboto', 15, 'bold')},
            default_font_settings={'font': ('Roboto', 12)},
            category_options=CATEGORYLIST,
            question_type_list=TYPELIST,
            difficulty_list=DIFFICULTLIST,
            user_default_category='Comunicação'
        )
        self.user_settings = dict(self._user_manager).copy()

    def save_user_settings(self, param: str, value: any) -> None:
        ic('update settings', param, value)
        if param in dict(self._user_manager).keys():
            self._user_manager.updatesetting(param, value)
