from pathlib import Path
from dataclasses import asdict
from itertools import groupby

from src.Constants import QUESTIOHEADER, QUESTIONTYPELIST, CATEGORYLIST, DIFFICULTLIST, D, TYPESCONVERTER
from src.contracts.model import ModelContract
from src.contracts.serializer import Serializer
from src.Hints.hints import SysImgHint, QuestionDataHint, ImageModelHint, UserSetHint, Any, Optional, Iterable, GroupedQuestionDBHint, ListDBHint, List
from src.Models.imagemodel import ImageModel
from src.Models.questionsdb import QuestionsDB
from src.Models.usermodel import UserModel
from src.Models.questionmodel import QuestionModel
from src.Models.Serializers.json_serializer import JsonSerializer
from src.Models.Serializers.binary_serializer import BinarySerializer
from src.Models.Serializers.xlsxserializer import XLSXSerializer


class Model(ModelContract):
    # ------ Initialization ------ #
    def __init__(self):
        self._base_dir = Path(__file__).resolve().parent.parent
        self._base_filename: Optional[str] = None
        self.__db_connection = QuestionsDB()
    # ------  ------ #

    # ------ Question Handling ------ #
    def create_new_question(self, question_data: QuestionDataHint) -> int:
        self._validate_question_data(question_data)

        question = QuestionModel(**question_data)

        control = self.__db_connection.create_question(question)

        if not control: raise ConnectionError('Não foi possível conectar se banco de dados')

        return control

    def read_question(self, control: int) -> QuestionDataHint:
        question = self.__db_connection.read_question(control)

        if not question: raise KeyError(f'Questão com controle: {control} inexistente')

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
                temp_question = question_data.copy()  # Crie um novo dicionário temporário
                del temp_question['alternativas']
                temp_question['tipo'] = TYPESCONVERTER.get(temp_question['tipo'])
                temp_question['alternativa'] = answer
                temp_question['correta'] = self._correct_onvert(correct, temp_question['tipo'])
                list_to_export.append(temp_question)

        self._save_file(file_path, list_to_export)

    def read_question_xlsx(self, filename: Path) -> GroupedQuestionDBHint:
        data: Iterable = self._read_file(filename)

        lines: ListDBHint = [dict(zip(QUESTIOHEADER, line)) for id_, line in enumerate(data) if id_]

        lista_dicionarios_ordenada = sorted(lines, key=lambda x: x['pergunta'])

        self._base_filename = filename.name

        return {chave: list(grupo) for chave, grupo in groupby(lista_dicionarios_ordenada, key=lambda x: x['pergunta'])}

    @staticmethod
    def _question_to_dict(all_questions: List[QuestionModel]) -> List[QuestionDataHint]:
        return [asdict(q) for q in all_questions]

    @staticmethod
    def _correct_onvert(correct: bool, type_: str):
        responses = {
            'me': 'CORRETA' if correct else '',
            'men': 'CORRETA' if correct else '',
            'vf': 'V' if correct else 'F',
            'd': ''
        }
        return responses.get(type_,'')
    # ------  ------ #

    # ------ System Images ------ #
    def read_system_images(self, image_names: ImageModelHint) -> SysImgHint:
        icons_dir = self._base_dir / 'icons'
        image_paths = {img_key: icons_dir / img_name for img_key, img_name in image_names.items()}

        self._img_manager = ImageModel(image_paths)
        return self._img_manager.get_images()
    # ------  ------ #

    # ------ User Settings ------ #
    def create_user_settings(self, configs_dir: Path) -> UserSetHint:
        self._user_settings = UserModel()

        self._save_file(configs_dir, dict(self._user_settings))

        return dict(self._user_settings)

    def read_user_settings(self, configs_dir: Path) -> UserSetHint:
        user_data = self._read_file(configs_dir)

        self._user_settings = UserModel(**user_data)
        return dict(self._user_settings)

    def update_user_settings(self, param: str, value: any, file_path: Path) -> None:
        if param in dict(self._user_settings).keys():
            self._user_settings.updatesetting(param, value)
            self._save_file(file_path, dict(self._user_settings))
            return
        raise KeyError(f'User setting "{param}" does not exist')
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
            case '.csv':
                pass
            case '.txt':
                pass
            case _:
                raise ValueError('Invalid extension!')

    def get_base_dir(self) -> Path:
        return self._base_dir

    def get_base_filename(self) -> str:
        return self._base_filename

    def get_current_file_path(self) -> Path:
        return self._base_dir / self._base_filename
    # ------  ------ #

    def _validate_question_data(self, data: QuestionDataHint) -> None:
        if not data: raise SyntaxError('Faltam informações para uma questão válida')

        # if self.read_question(data['controle']): KeyError('Questão já existente')

        if data['categoria'] not in CATEGORYLIST: raise KeyError(f'Categoria: {data['categoria']} deve ser um dos {CATEGORYLIST}')

        if len(data['tempo'].split(':')) != 3: raise KeyError(f'Tempo: {data['tempo']} com formato inválido deve ser 00:00:00')

        if data['tipo'] not in QUESTIONTYPELIST: raise KeyError(f'Tipo: {data['tipo']} deve ser um dos {QUESTIONTYPELIST}')

        if data['dificuldade'] not in DIFFICULTLIST: raise KeyError(f'Dificuldade: {data['dificuldade']} deve ser um dos {DIFFICULTLIST}')

        if not isinstance(data['peso'], int): raise ValueError(f'Peso {data['peso']} deve ser do tipo int')

        if not data['pergunta']: raise ValueError(f'Pergunta {data['pergunta']} não pode ser None')

        if data['tipo'] == D: return

        if len(data['alternativas']) > 1: raise ValueError('Perguntas de Multipla escolha e de verdadeiro ou false precisam ter ao menos duas opções')

        if not any([bool(choice) for choice, _ in data['alternativas']]): raise ValueError(f'Alternativa {data['alternativas']} não pode conter opçõa em branco')
