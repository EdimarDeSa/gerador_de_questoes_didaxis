from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image

from src.Hints.hints import Dict, SysImgHint


@dataclass(frozen=True)
class ImageModel:
    configuracoes_light_mode: Image.Image
    configuracoes_dark_mode: Image.Image
    eraser_light_mode: Image.Image
    eraser_dark_mode: Image.Image
    edit_light_mode: Image.Image
    edit_dark_mode: Image.Image
