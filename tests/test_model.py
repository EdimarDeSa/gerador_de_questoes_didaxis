from pathlib import Path

from src.Constants import CATEGORYLIST, DIFFICULTLIST
from src.model import Model


class TestModel:
    model = Model()
    created_questions = dict()

    def test_get_base_dir(self):
        entrada = self.model.get_base_dir()
        esperado = Path
        resultado = isinstance(entrada, esperado)
        assert resultado

    def test_get_base_filename(self):
        entrada = self.model.get_base_filename()
        esperado = None
        resultado = entrada is esperado
        assert resultado

    def test_create_me_question(self):
        for i, category in enumerate(CATEGORYLIST, 1):
            entrada = self.model.create_new_question({
                'id': None, 'categoria': category, 'subcategoria': None, 'controle': None,
                'tempo': f'{i:d2}:{i:d2}:{i:d2}', 'tipo': 'Multipla escolha 1 correta',
                'dificuldade': DIFFICULTLIST[i % len(DIFFICULTLIST)],
                'peso': i, 'pergunta': f'Pergunta {i}',
                'alternativas': [('Opção 1', False), ('Opção 2', True), ('Opção 3', False), ('Opção 4', False)]
            })
            esperado = i
            resultado = entrada == esperado
            assert resultado

