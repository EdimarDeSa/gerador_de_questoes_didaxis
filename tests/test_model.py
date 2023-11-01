from pathlib import Path
from random import choice

from pytest import raises

from src.Constants import CATEGORYLIST, DIFFICULTLIST
from src.Exceptions import QuestionValidationError
from src.model import Model


class TestModel:
    def setup_class(self):
        self.model = Model()
        self.created_questions = list()

    def test_get_base_dir(self):
        entrada = self.model.get_base_dir()

        esperado = True

        resultado = isinstance(entrada, Path)

        assert resultado == esperado

    def test_get_base_filename(self):
        entrada = self.model.get_base_filename()

        esperado = True

        resultado = entrada is None

        assert resultado == esperado

    def test_criacao_de_questoes_me_para_cada_categoria(self):
        for i, category in enumerate(CATEGORYLIST, 1):
            entrada = {
                'id': f'{i}',
                'categoria': category,
                'subcategoria': None,
                'tempo': f'{i:02}:{i:02}:{i:02}',
                'tipo': 'Multipla escolha 1 correta',
                'dificuldade': DIFFICULTLIST[i % len(DIFFICULTLIST)],
                'peso': i,
                'pergunta': f'Pergunta {i}',
                'alternativas': [
                    ('Opção 1', False),
                    ('Opção 2', True),
                    ('Opção 3', False),
                    ('Opção 4', False),
                ],
            }

            esperado = i

            resultado = self.model.create_new_question(entrada)

            entrada['controle'] = resultado

            self.created_questions.append(entrada)

            assert resultado == esperado

    def test_criacao_de_questoes_men_para_cada_categoria(self):
        total_ja_criada = len(self.created_questions) + 1
        for i, category in enumerate(CATEGORYLIST, total_ja_criada):
            entrada = {
                'id': f'{i}',
                'categoria': category,
                'subcategoria': None,
                'tempo': f'{i:02}:{i:02}:{i:02}',
                'tipo': 'Multipla escolha n corretas',
                'dificuldade': DIFFICULTLIST[i % len(DIFFICULTLIST)],
                'peso': i,
                'pergunta': f'Pergunta {i}',
                'alternativas': [
                    (f'Opção {idx}', choice([True, False])) for idx in range(4)
                ],
            }

            esperado = i

            resultado = self.model.create_new_question(entrada)

            entrada['controle'] = resultado

            self.created_questions.append(entrada)

            assert resultado == esperado

    def test_criacao_de_questoes_vf_para_cada_categoria(self):
        total_ja_criada = len(self.created_questions) + 1
        for i, category in enumerate(CATEGORYLIST, total_ja_criada):
            entrada = {
                'id': f'{i}',
                'categoria': category,
                'subcategoria': None,
                'tempo': f'{i:02}:{i:02}:{i:02}',
                'tipo': 'Verdadeiro ou falso',
                'dificuldade': DIFFICULTLIST[i % len(DIFFICULTLIST)],
                'peso': i,
                'pergunta': f'Pergunta {i}',
                'alternativas': [
                    (f'Opção {idx}', choice([True, False])) for idx in range(4)
                ],
            }

            esperado = i

            resultado = self.model.create_new_question(entrada)

            entrada['controle'] = resultado

            self.created_questions.append(entrada)

            assert resultado == esperado

    def test_criacao_de_questoes_d_para_cada_categoria(self):
        total_ja_criada = len(self.created_questions) + 1
        for i, category in enumerate(CATEGORYLIST, total_ja_criada):
            entrada = {
                'id': f'{i}',
                'categoria': category,
                'subcategoria': None,
                'tempo': f'{i:02}:{i:02}:{i:02}',
                'tipo': 'Dissertativa',
                'dificuldade': DIFFICULTLIST[i % len(DIFFICULTLIST)],
                'peso': i,
                'pergunta': f'Pergunta {i}',
                'alternativas': [('', False)],
            }

            esperado = i

            resultado = self.model.create_new_question(entrada)

            entrada['controle'] = resultado

            self.created_questions.append(entrada)

            assert resultado == esperado

    def test_leitura_das_questoes_armazenadas_no_banco_de_dados(self):
        for questao in self.created_questions:
            entrada = questao['controle']

            esperado = questao

            resultado = self.model.read_question(entrada)

            assert resultado == esperado

    def test_atualizacao_de_questao(self):
        for controle in [10, 15, 20, 25, 30, 35, 40, 45]:
            questao = self.model.read_question(controle)

            questao['pergunta'] = f'Pergunta alterada {controle}'

            self.model.update_question(questao)

            resultado = self.model.read_question(controle)

            assert (
                resultado == questao
            ), f'Deveria ter retornado {questao["pergunta"]} mas retornou {resultado["pergunta"]}'

    def test_validacao_de_sem_info_da_raise_questionvalidationerror(self):
        entrada = None

        with raises(QuestionValidationError):
            self.model._validate_question_data(entrada)

    def test_validacao_de_categoria_invalida_da_raise_questionvalidationerror(self):
        entrada = self.created_questions[0]

        entrada['categoria'] = 'Banana'

        with raises(QuestionValidationError):
            self.model._validate_question_data(entrada)

    def test_validacao_de_tempo_invalido_da_raise_questionvalidationerror(self):
        entrada = self.created_questions[0]

        entrada['tempo'] = 'Banana'

        with raises(QuestionValidationError):
            self.model._validate_question_data(entrada)

    def test_validacao_de_tipo_invalido_da_raise_questionvalidationerror(self):
        entrada = self.created_questions[0]

        entrada['tipo'] = 'Banana'

        with raises(QuestionValidationError):
            self.model._validate_question_data(entrada)

    def test_validacao_de_dificuldade_invalido_da_raise_questionvalidationerror(self):
        entrada = self.created_questions[0]

        entrada['dificuldade'] = 'Banana'

        with raises(QuestionValidationError):
            self.model._validate_question_data(entrada)

    def test_validacao_de_peso_invalido_da_raise_questionvalidationerror(self):
        entrada = self.created_questions[0]

        entrada['peso'] = 'Banana'

        with raises(QuestionValidationError):
            self.model._validate_question_data(entrada)

    def test_validacao_de_pergunta_invalido_da_raise_questionvalidationerror(self):
        entrada = self.created_questions[0]

        entrada['pergunta'] = None

        with raises(QuestionValidationError):
            self.model._validate_question_data(entrada)

    def test_validacao_de_alternativas_devem_ter_mais_de_duas_ou_da_raise_questionvalidationerror(self):
        entrada = self.created_questions[0]

        entrada['alternativas'] = [('', False)]

        with raises(QuestionValidationError):
            self.model._validate_question_data(entrada)

    def test_validacao_de_alternativas_nao_devem_conter_opcoes_em_branco_da_raise_questionvalidationerror(self):
        entrada = self.created_questions[0]

        entrada['alternativas'] = [('', False), ('Banana', True)]

        with raises(QuestionValidationError):
            self.model._validate_question_data(entrada)

    def test_validacao_de_alternativas_me_devem_conter_apenas_um_correta_ou_da_raise_questionvalidationerror(self):
        entrada = self.created_questions[0]

        entrada['alternativas'] = [('Banana 1', True), ('Banana 2', True)]

        with raises(QuestionValidationError):
            self.model._validate_question_data(entrada)

    def test_validacao_de_tipo_dissertativa_deve_retornar_none(self):
        entrada = self.created_questions[1]

        entrada['tipo'] = 'Dissertativa'

        esperado = None

        resultado = self.model._validate_question_data(entrada)

        assert resultado == esperado

    def test_exclusao_de_questao_por_controle(self):
        for controle in [10, 15, 20, 25, 30, 35, 40, 45]:

            self.model.delete_question(controle)

            self.created_questions.pop(controle - 1)

            with raises(KeyError):
                self.model.read_question(controle)

    def test_flush_de_questoes(self):
        self.model.flush_questions()

        for questao in self.created_questions:
            entrada = questao['controle']

            with raises(KeyError):
                self.model.read_question(entrada)

    def test_reset_do_base_file_name_apos_flush(self):
        entrada = self.model.get_base_filename

        esperado = None

        resultado = entrada()

        assert resultado == esperado
