from pathlib import Path
from PIL import Image
from dataclasses import dataclass, field

from src.Hints.hints import SysImgHint, Dict
from src.Constants import CATEGORYLIST, QUESTIONTYPELIST, DIFFICULTLIST




@dataclass(kw_only=True)
class ImageManager:
    icons_dir: Path
    image_paths: Dict[str, str]

    def __post_init__(self):
        self._images = {name: self._abre_imagem(path) for name, path in self.image_paths.items()}

    def _abre_imagem(self, nome_imagem: str) -> Image:
        caminho_imagem = self.icons_dir / nome_imagem
        return Image.open(caminho_imagem)

    def get_images(self) -> SysImgHint:
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
        self.base_dir = Path(__file__).resolve().parent.parent

        icons_dir = self.base_dir / 'icons'
        self._img_manager = ImageManager(icons_dir=icons_dir, image_paths={
            'configuracoes_light_mode': 'configuracoes_light_mode.png',
            'configuracoes_dark_mode': 'configuracoes_dark_mode.png',
            'eraser_light_mode': 'eraser_light_mode.png',
            'eraser_dark_mode': 'eraser_dark_mode.png',
            'edit_light_mode': 'edit_light_mode.png',
            'edit_dark_mode': 'edit_dark_mode.png',
        })
        self.system_images: SysImgHint = self._img_manager.get_images()

        configs_dir = self.base_dir / 'configs'
        self._user_manager = UserManager(
            titles_font_settings={'font': ('Roboto', 15, 'bold')},
            default_font_settings={'font': ('Roboto', 12)},
            category_options=CATEGORYLIST,
            question_type_list=QUESTIONTYPELIST,
            difficulty_list=DIFFICULTLIST,
            user_default_category='Comunicação'
        )
        self.user_settings = dict(self._user_manager).copy()

    def save_user_settings(self, param: str, value: any) -> None:
        # print('update settings', param, value)
        if param in dict(self._user_manager).keys():
            self._user_manager.updatesetting(param, value)
