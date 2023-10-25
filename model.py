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
SUBCATEGORYLIST = [FACIL, MEDIO, DIFICIL]


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
    erase_statement: bool
    auto_export: bool
    user_color_theme: str = field(default='green')
    user_scaling: str = field(default='100%')
    user_appearance_mode: str = field(default='system')
    titles_font_settings: dict = field(default_factory=dict)
    default_font_settings: dict = field(default_factory=dict)

    def get_settings(self) -> dict:
        return self.__dict__


class Model:
    category_options = CATEGORYLIST
    question_type_list = TYPELIST
    difficulty_list = SUBCATEGORYLIST

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
            erase_statement=False,
            auto_export=False,
            user_color_theme=COLORTHEMELIST[2],
            user_scaling=SCALESTHEMELIST[2],
            user_appearance_mode=APPEARANCEMODETHEME[2],
            titles_font_settings={'font': ('Roboto', 15, 'bold')},
            default_font_settings={'font': ('Roboto', 12)},
        )
        self.user_settings = self._user_manager.get_settings()

        self.titles_font_settings = self._user_manager.titles_font_settings
        self.default_font_settings = self._user_manager.default_font_settings
        self.user_appearance_mode = self._user_manager.user_appearance_mode
        self.user_scaling = self._user_manager.user_scaling
        self.user_color_theme = self._user_manager.user_color_theme

    def save_user_settings(self, param: str, value: any) -> None:
        if param in self._user_manager.__dict__.keys():
            self._user_manager.__dict__.update({param: value})
