from pathlib import Path
from PIL import Image

from dataclasses import dataclass
from src.Hints.hints import SysImgHint, Dict


@dataclass
class ImageModel:
    image_paths: Dict[str, Path]

    def __post_init__(self):
        self._images = {name: self._abre_imagem(path) for name, path in self}

    def _abre_imagem(self, image_path: Path) -> Image:
        return Image.open(image_path)

    def get_images(self) -> SysImgHint:
        return self._images

    def __iter__(self):
        return iter(self.image_paths.items())
