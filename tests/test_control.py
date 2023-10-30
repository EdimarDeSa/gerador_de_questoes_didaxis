import random

from src.controller import Controller
from src.ctkview import CTkView
from src.model import Model
from src.Constants import D, VF, ME, MEN, CATEGORYLIST, DIFFICULTLIST, QUESTIONTYPELIST


class TestController:
    def test_main(self):
        view = CTkView()
        model = Model()
        controls = Controller(view, model)

        controls.start()

        for i in range(50):
            random_tipo = random.choice(QUESTIONTYPELIST)
            random_dificuldade = random.choice(DIFFICULTLIST)
            random_peso = random.randint(1, 50)  # Gere um peso aleatório entre 1 e 10
            random_categoria = random.choice(CATEGORYLIST)
            alternativas = [
                (f'op {j}', random.choice([True, False])) for j in range(1, 5)
            ]
            view.insert_data_in_question_form({
                'id': str(i),
                'categoria': random_categoria,
                'subcategoria': random_categoria,
                'controle': i,
                'tempo': '00:00:00',
                'tipo': random_tipo,
                'dificuldade': random_dificuldade,
                'peso': random_peso,
                'pergunta': f'Pergunta {i}',
                'alternativas': alternativas
            })
            view.create_question()


        controls.loop(True)
