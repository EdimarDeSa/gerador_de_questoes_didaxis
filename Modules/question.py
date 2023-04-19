from typing import List

class Question:
    def __init__(self, unit: str, code: str, time: str, type_: str, difficulty: str, weight: str, question: str,
                 options: List[tuple]):
        """Construct a new Question"""
        self.unit = unit.capitalize()
        self.code = code
        self.time = time
        self.type_ = type_
        self.difficulty = difficulty.capitalize()
        self.weight = int(weight)
        self.question = question.capitalize()
        self.options = options

    def __str__(self) -> str:
        options_str = ', '.join([f'({letter}) {text}' for letter, text in self.options])
        return f'Unit: {self.unit}\n' \
               f'Code: {self.code}\n' \
               f'Time: {self.time}\n' \
               f'Type: {self.type_}\n' \
               f'Difficulty: {self.difficulty}\n' \
               f'Weight: {self.weight}\n' \
               f'Question: {self.question}\n' \
               f'Options: {options_str}'

    def __repr__(self) -> str:
        return f'<Question: {self.question}>'
