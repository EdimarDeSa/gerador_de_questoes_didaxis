from dataclasses import asdict, replace
from itertools import groupby
from pathlib import Path

from PIL import Image

from .Constants import (
    CATEGORYLIST,
    DIFFICULTLIST,
    ME,
    MEN,
    QUESTIOHEADER,
    QUESTIONTYPELIST,
    TYPESCONVERTER,
    VF,
    D,
)
from .Contracts.modelcontract import ModelContract
from .Contracts.serializerhandlers import Serializer
from .DataModels.imagemodel import ImageModel
from .DataModels.questionmodel import QuestionModel
from .DataModels.questionsdb import QuestionsDB
from .DataModels.usermodel import UserModel
from .Exceptions import QuestionValidationError
from .Hints.hints import (
    Any,
    GroupedQuestionDBHint,
    ImageModelHint,
    Iterable,
    List,
    ListDBHint,
    Optional,
    QuestionDataHint,
)
from .Serializers.binary_serializer import BinarySerializer
from .Serializers.json_serializer import JsonSerializer
from .Serializers.xlsxserializer import XLSXSerializer


class Model(ModelContract):
    # ------ Initialization ------ #
    def __init__(self) -> None:
        self._base_dir = Path(__file__).resolve().parent.parent
        self._base_filename: Optional[str] = None
        self.__db_connection = QuestionsDB()

    # ------  ------ #

    # ------ Question Handling ------ #
    def create_new_question(self, question_data: QuestionDataHint) -> int:
        """
        Notes:
            Valida as informações da questão para então gerar um objeto :class: QuestionModel
            com os dados e os armazena no banco de dados.

        Args:
            question_data: Dados da questão

        :type question_data: QuestionDataHint
        :return: Número do controle da questão (identificador genérico)
        :rtype: int

        Examples:
            Testando exemplos

            >>> self.create_new_question({ 'id': None, 'categoria': 'Comunicação', 'subcategoria': None, 'tempo': '00:00:00', 'tipo': 'Multipla escolha 1 correta', 'dificuldade': 'Fácil', 'peso': 1, 'pergunta': 'Pergunta 1', 'controle': None, 'alternativas': [('Opção 1', False), ('Opção 2', True), ('Opção 3', False), ('Opção 4', False)]})
            1
        """
        self._validate_question_data(question_data)

        question = QuestionModel(**question_data)

        control = self.__db_connection.create_question(question)

        if not control:
            raise ConnectionError('Não foi possível conectar se banco de dados')

        return control

    def read_question(self, control: int) -> QuestionDataHint:
        question = self.__db_connection.read_question(control)

        if not question:
            raise KeyError(f'Questão com controle: {control} inexistente')

        return asdict(question)

    def update_question(self, question_data: QuestionDataHint) -> None:
        self._validate_question_data(question_data)

        self.__db_connection.update_question(question_data)

    @staticmethod
    def _validate_question_data(data: QuestionDataHint) -> None:
        if not data:
            raise QuestionValidationError(
                'Faltam informações para uma questão válida.\n'
                f'{str(QuestionDataHint)}.'
            )

        if data['categoria'] not in CATEGORYLIST:
            raise QuestionValidationError(
                f'Categoria `{data["categoria"]}` deve ser uma da lista {CATEGORYLIST}.'
            )

        if len(data['tempo'].split(':')) != 3:
            raise QuestionValidationError(
                f'Tempo `{data["tempo"]}` com formato inválido deve ser hh:mm:ss.'
            )

        if data['tipo'] not in QUESTIONTYPELIST:
            raise QuestionValidationError(
                f'Tipo `{data["tipo"]}` deve ser um da lista {QUESTIONTYPELIST}.'
            )

        if data['dificuldade'] not in DIFFICULTLIST:
            raise QuestionValidationError(
                f'Dificuldade `{data["dificuldade"]}` deve ser uma da lista {DIFFICULTLIST}.'
            )

        if not isinstance(data['peso'], int):
            raise QuestionValidationError(f'Peso `{data["peso"]}` deve ser numérico.')

        if not data['pergunta']:
            raise QuestionValidationError(f'Perguntas não podem estar em branco.')

        if data['tipo'] == D:
            return

        if len(data['alternativas']) < 2:
            raise QuestionValidationError(
                f'Perguntas {data["tipo"]} precisam ter ao menos duas opções!'
            )

        if not any([bool(choice) for choice, _ in data['alternativas']]):
            raise QuestionValidationError(
                f'Alternativas não podem conter opção em branco.'
            )

        if data['tipo'] == ME:
            count = 0
            for _, correta in data['alternativas']:
                if correta:
                    count += 1

            if 0 == count > 1:
                raise QuestionValidationError(
                    f'Alternativas de questoes `{data["tipo"]}` devem conter exclusivamente 1 questão correta.'
                )

    def delete_question(self, control: int) -> None:
        try:
            self.__db_connection.delete_question(control)

        except ConnectionError:
            raise ConnectionError('Nãofoi possível se conectar ao banco de dados.')

    def flush_questions(self) -> None:
        self.__db_connection.flush_questions()
        self._base_filename = None

    # ------  ------ #

    # ------ Questions xlsx Handler ------ #
    def get_questions_to_export_xlsx(self) -> List[QuestionDataHint]:
        all_questions = self.__db_connection.select_all_questions()

        dict_of_questions = self._each_question_to_dict(all_questions)
        all_questions = None

        list_to_export = list()
        for question_data in dict_of_questions:
            intermedite_temp_question = question_data.copy()

            intermedite_temp_question['tipo'] = TYPESCONVERTER.get(
                question_data['tipo']
            )

            del intermedite_temp_question['alternativas']

            if intermedite_temp_question['tipo'] == 'd':
                intermedite_temp_question['alternativa'] = ''
                intermedite_temp_question['correta'] = ''

                list_to_export.append(intermedite_temp_question)
                continue

            for answer, correct in question_data['alternativas']:
                final_temp_question = intermedite_temp_question.copy()
                final_temp_question['alternativa'] = answer
                final_temp_question['correta'] = self._correct_onvert(
                    correct, question_data['tipo']
                )
                list_to_export.append(final_temp_question)
        return list_to_export

    def read_question_xlsx(self, filename: Path) -> GroupedQuestionDBHint:
        data: Iterable = self._read_file(filename)

        lines: ListDBHint = [
            dict(zip(QUESTIOHEADER, line)) for id_, line in enumerate(data) if id_
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
    def _each_question_to_dict(
        all_questions: List[QuestionModel],
    ) -> List[QuestionDataHint]:
        return [asdict(q) for q in all_questions]

    @staticmethod
    def _correct_onvert(correct: bool, type_: str) -> bool:
        responses = {
            ME: 'CORRETA' if correct else '',
            MEN: 'CORRETA' if correct else '',
            VF: 'V' if correct else 'F',
            D: '',
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

        self.save_file(configs_dir, asdict(user_settings))

    def read_user_settings(self, configs_dir: Path) -> UserModel:
        user_data = self._read_file(configs_dir)

        self._user_settings = UserModel(**user_data)
        return self._user_settings

    def update_user_settings(self, file_path: Path, **new_config) -> UserModel:
        for key in new_config:
            if key in asdict(self._user_settings):
                self._user_settings = replace(self._user_settings, **new_config)
                self.save_file(file_path, asdict(self._user_settings))
                return self._user_settings
            raise KeyError(f'User setting "{key}" does not exist')

    # ------  ------ #

    # ------ File Handling and Serialization ------ #
    def create_path(self, filename: str) -> Path:
        return self._base_dir / filename

    def _read_file(self, file_path: Path) -> Any:
        serializer = self._select_serializer(file_path)
        return serializer.import_from_path(file_path)

    def save_file(self, file_path: Path, data: Any) -> None:
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

    def register_file_path(self, file_path: Path) -> None:
        self._base_dir = file_path.parent
        self._base_filename = file_path.name

    def create_personal_dict(self, default_dict_path: Path, file_path: Path) -> None:
        default_dict: str = self._read_file(default_dict_path)
        self.save_file(file_path, default_dict.split('\n'))

    # ------  ------ #
