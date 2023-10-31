# import sqlite3
from dataclasses import replace

from src.contracts.questionsdbcontrct import QuestionDBContract
from src.Hints.hints import Dict, List, QuestionDataHint

from .questionmodel import QuestionModel


class QuestionsDB(QuestionDBContract):
    def __init__(self):
        self.__db: Dict[int, QuestionModel] = dict()
        self.__control = 0

    def create_question(self, question_data: QuestionModel) -> int:
        control = self._next_control()

        question = replace(question_data, controle=control)

        self.__db[control] = question

        return question.controle

    def read_question(self, control: int) -> QuestionModel:
        return self.__db.get(control)

    def update_question(self, question: QuestionDataHint) -> None:
        current_qeuestion = self.__db.get(question['controle'])
        self.__db[question['controle']] = replace(
            current_qeuestion, **question
        )

    def delete_question(self, control: int) -> None:
        del self.__db[control]

    def flush_questions(self) -> None:
        self.__db.clear()
        self.__control = 0

    def select_all_questions(self) -> List[QuestionModel]:
        return [question for question in self.__db.values()]

    def _next_control(self) -> int:
        self.__control += 1
        return self.__control
