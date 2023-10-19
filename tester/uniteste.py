import unittest
from Modules.funcoes import AbrirArquivo


class TestAbrirArquivo(unittest.TestCase):
    def test_get_desktop_path(self):
        # Testa o método get_desktop_path
        desktop_path = AbrirArquivo.get_desktop_path()
        self.assertTrue(desktop_path.is_dir())

    # Adicione mais métodos de teste para os outros métodos da classe


if __name__ == '__main__':
    unittest.main()
