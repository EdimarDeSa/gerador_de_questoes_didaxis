# import sqlite3

from icecream import ic

from src.contracts.questionsdbcontrct import QuestionDBContract
from .questionmodel import QuestionModel
from src.Hints.hints import Dict, List, QuestionDataHint


class QuestionsDB(QuestionDBContract):
    def __init__(self):
        self.__db: Dict[int, QuestionModel] = dict()
        self.__control = 0

    def create_question(self, question_data: QuestionDataHint) -> int:
        control = self._next_control()
        question_data['controle'] = control
        question = QuestionModel(**question_data)
        self.__db[control] = question
        return control

    def read_question(self, control: int) -> QuestionDataHint:
        question = self.__db.get(control, None)
        return dict(question)

    def update_question(self, question: QuestionDataHint) -> None:
        self.__db[question['controle']].update(**question)

    def delete_question(self, control: int) -> None:
        del self.__db[control]

    def flush_questions(self) -> None:
        self.__db.clear()
        self.__control = 0

    def select_all_questions(self) -> List[QuestionDataHint]:
        return [dict(question) for question in self.__db.values()]

    def _next_control(self) -> int:
        self.__control += 1
        return self.__control
