from dataclasses import asdict, replace
from itertools import groupby
from pathlib import Path

from PIL import Image

from src.Constants import (
    CATEGORYLIST,
    DIFFICULTLIST,
    ME,
    QUESTIOHEADER,
    QUESTIONTYPELIST,
    TYPESCONVERTER,
    D,
)
from src.contracts.model import ModelContract
from src.contracts.serializer import Serializer
from src.DataModels.imagemodel import ImageModel
from src.DataModels.questionmodel import QuestionModel
from src.DataModels.questionsdb import QuestionsDB
from src.DataModels.usermodel import UserModel
from src.Exceptions import QuestionValidationError
from src.Hints.hints import (
    Any,
    GroupedQuestionDBHint,
    ImageModelHint,
    Iterable,
    List,
    ListDBHint,
    Optional,
    QuestionDataHint,
)
from src.Serializers.binary_serializer import BinarySerializer
from src.Serializers.json_serializer import JsonSerializer
from src.Serializers.xlsxserializer import XLSXSerializer


class Model(ModelContract):
    # ------ Initialization ------ #
    def __init__(self):
        self._base_dir = Path(__file__).resolve().parent.parent
        self._base_filename: Optional[str] = None
        self.__db_connection = QuestionsDB()

    # ------  ------ #

    # ------ Question Handling ------ #
    def create_new_question(self, question_data: QuestionDataHint) -> int:
        """
        Valida  as informações da questão, gera um objeto com os dados e armazena no banco de dados.
        :param question_data: Dados da questão
        :type question_data: QuestionDataHint
        :return: Número do controle da questão (identificador genérico)
        :rtype: int

        >>> create_new_question({ 'id': None, 'categoria': 'Comunicação', 'subcategoria': None, 'tempo': '00:00:00', 'tipo': 'Multipla escolha 1 correta', 'dificuldade': 'Fácil', 'peso': 1, 'pergunta': 'Pergunta 1', 'alternativas': [('Opção 1', False), ('Opção 2', True), ('Opção 3', False), ('Opção 4', False)] }) 1
        """
        self._validate_question_data(question_data)

        question = QuestionModel(**question_data)

        control = self.__db_connection.create_question(question)

        if not control:
            raise ConnectionError(
                'Não foi possível conectar se banco de dados'
            )

        return control

    def read_question(self, control: int) -> QuestionDataHint:
        question = self.__db_connection.read_question(control)

        if not question:
            raise KeyError(f'Questão com controle: {control} inexistente')

        return asdict(question)

    def update_question(self, question_data: QuestionDataHint) -> None:
        self._validate_question_data(question_data)

        self.__db_connection.update_question(question_data)

    def delete_question(self, control: int) -> None:
        self.__db_connection.delete_question(control)

    def flush_questions(self) -> None:
        self.__db_connection.flush_questions()
        self._base_dir = Path.home() / 'Desktop'
        self._base_filename = None

    # ------  ------ #

    # ------ Questions xlsx Handler ------ #
    def create_question_xlsx(self, file_path: Path) -> None:
        all_questions = self.__db_connection.select_all_questions()

        dict_of_questions = self._question_to_dict(all_questions)

        list_to_export = list()
        for question_data in dict_of_questions:
            alternativas = question_data['alternativas']
            for answer, correct in alternativas:
                temp_question = (
                    question_data.copy()
                )  # Crie um novo dicionário temporário
                del temp_question['alternativas']
                temp_question['tipo'] = TYPESCONVERTER.get(
                    temp_question['tipo']
                )
                temp_question['alternativa'] = answer
                temp_question['correta'] = self._correct_onvert(
                    correct, temp_question['tipo']
                )
                list_to_export.append(temp_question)

        self._save_file(file_path, list_to_export)

    def read_question_xlsx(self, filename: Path) -> GroupedQuestionDBHint:
        data: Iterable = self._read_file(filename)

        lines: ListDBHint = [
            dict(zip(QUESTIOHEADER, line))
            for id_, line in enumerate(data)
            if id_
        ]

        lista_dicionarios_ordenada = sorted(lines, key=lambda x: x['pergunta'])

        self._base_filename = filename.name

        return {
            chave: list(grupo)
            for chave, grupo in groupby(
                lista_dicionarios_ordenada, key=lambda x: x['pergunta']
            )
        }

    @staticmethod
    def _question_to_dict(
        all_questions: List[QuestionModel],
    ) -> List[QuestionDataHint]:
        return [asdict(q) for q in all_questions]

    @staticmethod
    def _correct_onvert(correct: bool, type_: str):
        responses = {
            'me': 'CORRETA' if correct else '',
            'men': 'CORRETA' if correct else '',
            'vf': 'V' if correct else 'F',
            'd': '',
        }
        return responses.get(type_, '')

    # ------  ------ #

    # ------ System Images ------ #
    def read_system_images(self, image_names: ImageModelHint) -> ImageModel:
        images_dict = {
            key: Image.open(img_path) for key, img_path in image_names.items()
        }
        return ImageModel(**images_dict)

    # ------  ------ #

    # ------ User Settings ------ #
    def create_user_settings(self, configs_dir: Path) -> None:
        user_settings = UserModel(
            category_options=CATEGORYLIST,
            question_type_list=QUESTIONTYPELIST,
            difficulty_list=DIFFICULTLIST,
        )

        self._save_file(configs_dir, asdict(user_settings))

    def read_user_settings(self, configs_dir: Path) -> UserModel:
        user_data = self._read_file(configs_dir)

        self._user_settings = UserModel(**user_data)
        return self._user_settings

    def update_user_settings(self, file_path: Path, **new_config) -> None:
        for key in new_config.keys():
            if key in asdict(self._user_settings):
                self._user_settings = replace(
                    self._user_settings, **new_config
                )
                self._save_file(file_path, asdict(self._user_settings))
                return
            raise KeyError(f'User setting "{key}" does not exist')

    # ------  ------ #

    # ------ File Handling and Serialization ------ #
    def create_path(self, filename: str) -> Path:
        return self._base_dir / filename

    def _read_file(self, file_path: Path) -> Any:
        serializer = self._select_serializer(file_path)
        return serializer.import_from_path(file_path)

    def _save_file(self, file_path: Path, data: Any):
        serializer = self._select_serializer(file_path)
        serializer.export_to_path(file_path, data)

    @staticmethod
    def _select_serializer(filename: Path) -> Serializer:
        match filename.suffix.lower():
            case '.json':
                return JsonSerializer()
            case '.bin':
                return BinarySerializer()
            case '.xlsx':
                return XLSXSerializer()
            case _:
                raise ValueError('Invalid extension!')

    def get_base_dir(self) -> Path:
        return self._base_dir

    def get_base_filename(self) -> str:
        return self._base_filename

    def get_current_file_path(self) -> Path:
        return self._base_dir / self._base_filename

    # ------  ------ #

    @staticmethod
    def _validate_question_data(data: QuestionDataHint) -> None:
        if not data:
            raise QuestionValidationError(
                'Faltam informações para uma questão válida'
            )

        if data['categoria'] not in CATEGORYLIST:
            raise QuestionValidationError(
                f'Categoria: {data["categoria"]} deve ser um dos {CATEGORYLIST}'
            )

        if len(data['tempo'].split(':')) != 3:
            raise QuestionValidationError(
                f'Tempo: {data["tempo"]} com formato inválido deve ser 00:00:00'
            )

        if data['tipo'] not in QUESTIONTYPELIST:
            raise QuestionValidationError(
                f'Tipo: {data["tipo"]} deve ser um dos {QUESTIONTYPELIST}'
            )

        if data['dificuldade'] not in DIFFICULTLIST:
            raise QuestionValidationError(
                f'Dificuldade: {data["dificuldade"]} deve ser um dos {DIFFICULTLIST}'
            )

        if not isinstance(data['peso'], int):
            raise QuestionValidationError(
                f'Peso {data["peso"]} deve ser do tipo int'
            )

        if not data['pergunta']:
            raise QuestionValidationError(
                f'Pergunta {data["pergunta"]} não pode ser None'
            )

        if data['tipo'] == D:
            return

        if len(data['alternativas']) < 2:
            raise QuestionValidationError(
                'Perguntas de Multipla escolha e de verdadeiro ou false precisam ter ao menos duas opções'
            )

        if not any([bool(choice) for choice, _ in data['alternativas']]):
            raise QuestionValidationError(
                f'Alternativa {data["alternativas"]} não pode conter opçõa em branco'
            )

        if data['tipo'] == ME:
            count = 0
            for _, correta in data['alternativas']:
                if correta:
                    count += 1

            if 0 == count > 1:
                raise QuestionValidationError(
                    f'Alternativas de questoes {ME} devem conter exclusivamente 1 questão correta.'
                )
