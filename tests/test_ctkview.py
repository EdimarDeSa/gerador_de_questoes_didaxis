from src.controller import Controller
from src.ctkview import CTkView
from src.model import Model

from src.Constants import DIFFICULTLIST, QUESTIONTYPELIST, CATEGORYLIST


class TestClass:
    def test_start(self):
        view = CTkView()
        model = Model()
        controls = Controller(view, model)
        controls.start()

        for i, category in enumerate(CATEGORYLIST, 1):
            inserted_question = dict(
                categoria=category,
                subcategoria=f'{category[:5]}-P5502',
                controle=i,
                tempo=f'0{i}:0{i+1}:0{i+2}',
                tipo=QUESTIONTYPELIST[i % 4],
                dificuldade=DIFFICULTLIST[i % 3],
                peso=i,
                pergunta=f'Pergunta teste {i}',
                alternativas=[(f'Op teste 1 - Pergunta {i}', True),
                              (f'Op teste 2 - Pergunta {i}', False),
                              (f'Op teste 3 - Pergunta {i}', True),
                              (f'Op teste 4 - Pergunta {i}', False)]
            )
            view.insert_data_in_question_form(inserted_question)

            view.create_question()
        view.tests()

        for i in range(10):
            collectes_question = controls.read_question_handler(i)

            assert collectes_question['categoria'] == inserted_question['categoria']
            assert collectes_question['subcategoria'] == inserted_question['subcategoria']
            assert collectes_question['tempo'] == inserted_question['tempo']
            assert collectes_question['tipo'] == inserted_question['tipo']
            # assert collectes_question['controle'] == inserted_question['controle']
            assert collectes_question['dificuldade'] == inserted_question['dificuldade']
            assert collectes_question['peso'] == inserted_question['peso']
            assert collectes_question['pergunta'] == inserted_question['pergunta']
            assert collectes_question['alternativas'] == inserted_question['alternativas']
        controls.loop()

