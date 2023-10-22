from customtkinter import CTkImage
from pathlib import Path
from PIL import Image


class ImageManager:
    def __init__(self, base_dir: Path):
        self._ICONS_DIR = base_dir / 'icons'

        self.bt_delete = self._bt_deletar_questao_img()
        self.bt_edit = self._bt_editar_questao_img()
        self.bt_configs = self._bt_configs_img()

    def _bt_configs_img(self) -> CTkImage:
        bt_configs_img_light_mode = self._abre_imagem('configuracoes_light_mode.png')
        bt_configs_img_dark_mode = self._abre_imagem('configuracoes_dark_mode.png')
        bt_configs_img = CTkImage(bt_configs_img_light_mode, bt_configs_img_dark_mode, (24, 24))
        return bt_configs_img

    def _bt_deletar_questao_img(self) -> CTkImage:
        eraser_light_mode = self._abre_imagem('eraser_light_mode.png')
        eraser_dark_mode = self._abre_imagem('eraser_dark_mode.png')
        bt_deletar_questao = CTkImage(eraser_light_mode, eraser_dark_mode, (16, 16))
        return bt_deletar_questao

    def _bt_editar_questao_img(self) -> CTkImage:
        edit_light_mode = self._abre_imagem('edit_light_mode.png')
        edit_dark_mode = self._abre_imagem('edit_dark_mode.png')
        bt_editar_questao = CTkImage(edit_light_mode, edit_dark_mode, (16, 16))
        return bt_editar_questao

    def _abre_imagem(self, nome_imagem: str) -> Image:
        caminho_imagem = self._ICONS_DIR / nome_imagem
        return Image.open(caminho_imagem)
