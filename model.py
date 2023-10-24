from icecream import ic


# Unidades de negócio
ASTEC = 'astec'
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
CATEGORYLIST = [ASTEC, COMUNICACAO, CONTROLE, ENERGIA, EXPORTACAO, GESTAO, INCENDIO, NEGOCIOS, REDES, SEGURANCA, SOLAR,
                SOLUCOES, VAREJO, VERTICAIS]

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


class ImageManager:
    def __init__(self, base_dir: Path):
        self._icons_dir = base_dir / 'icons'

        self.setup_bt_img_light = self._abre_imagem('configuracoes_light_mode.png')
        self.setup_bt_img_dark = self._abre_imagem('configuracoes_dark_mode.png')

        self.eraser_light = self._abre_imagem('eraser_light_mode.png')
        self.eraser_dark = self._abre_imagem('eraser_dark_mode.png')

        self.edit_light = self._abre_imagem('edit_light_mode.png')
        self.edit_dark = self._abre_imagem('edit_dark_mode.png')

    def _abre_imagem(self, nome_imagem: str) -> Image:
        caminho_imagem = self._icons_dir / nome_imagem
        return Image.open(caminho_imagem)


class Model:
    # User settings
    titles_font_settings = {'font': ('Roboto', 15, 'bold')}
    default_font_settings = {'font': ('Roboto', 12)}
    user_color_theme = COLORTHEMELIST[2]
    user_scaling = SCALESTHEMELIST[2]
    user_appearance_mode = APPEARANCEMODETHEME[2]

    # Options list
    category_options = CATEGORYLIST
    question_type_list = TYPELIST
    difficulty_list = SUBCATEGORYLIST

    def __init__(self):
        local = Path().resolve()
        self._img_manager = ImageManager(local)

        self.setup_bt_img_light = self._img_manager.setup_bt_img_light
        self.setup_bt_img_dark = self._img_manager.setup_bt_img_dark
        self.eraser_light = self._img_manager.eraser_light
        self.eraser_dark = self._img_manager.eraser_dark
        self.edit_light = self._img_manager.edit_light
        self.edit_dark = self._img_manager.edit_dark
        
        