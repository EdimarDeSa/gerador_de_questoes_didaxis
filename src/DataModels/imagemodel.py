from dataclasses import dataclass

from ..Hints import ImageType


@dataclass
class ImageModel:
    configuracoes_light_mode: ImageType
    configuracoes_dark_mode: ImageType
    eraser_light_mode: ImageType
    eraser_dark_mode: ImageType
    edit_light_mode: ImageType
    edit_dark_mode: ImageType
