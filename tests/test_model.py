from PIL import Image

from src.model import Model


class TestModel:
    def test_open_images(self):
        model = Model()

        image_paths = {
            'configuracoes_light_mode': 'configuracoes_light_mode.png',
            'configuracoes_dark_mode': 'configuracoes_dark_mode.png',
            'eraser_light_mode': 'eraser_light_mode.png',
            'eraser_dark_mode': 'eraser_dark_mode.png',
            'edit_light_mode': 'edit_light_mode.png',
            'edit_dark_mode': 'edit_dark_mode.png',
        }
        system_images = model.read_system_images(image_paths)

        for image in system_images.values():
            assert isinstance(image, Image.Image)
