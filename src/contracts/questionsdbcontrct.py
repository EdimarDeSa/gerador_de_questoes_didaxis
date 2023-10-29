from abc import ABC, abstractmethod

from src.Hints.hints import List, QuestionDataHint


class QuestionDBContract(ABC):
    @abstractmethod
    def create_question(self, question_data: QuestionDataHint) -> int:
        pass

    @abstractmethod
    def read_question(self, control: int) -> QuestionDataHint:
        pass

    @abstractmethod
    def update_question(self, question: QuestionDataHint) -> None:
        pass

    @abstractmethod
    def delete_question(self, control: int) -> None:
        pass

    @abstractmethod
    def flush_questions(self) -> None:
        pass

    @abstractmethod
    def select_all_questions(self) -> List[QuestionDataHint]:
        pass
