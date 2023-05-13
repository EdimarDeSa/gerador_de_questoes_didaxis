from typing import List


class SettersMeta(type):
    def __new__(cls, name, bases, attrs):
        for attr_name, attr_value in attrs.items():
            if not attr_name.startswith('__') and not callable(attr_value):
                setter_name = 'set_' + attr_name
                attrs[setter_name] = property(lambda self, value, name=attr_name: setattr(self, name, value))
        return super().__new__(cls, name, bases, attrs)


class Question():
    def __init__(self):
        """Construct a new Question"""
        self.__unit = None
        self.__code = None
        self.__time = None
        self.__type_ = None
        self.__difficulty = None
        self.__weight = None
        self.__question = None
        self.__options = None
    
    @property
    def unit(self):
        return self.__unit
    
    @property
    def code(self):
        return self.__code

    @property
    def time(self):
        return self.__time

    @property
    def type_(self):
        return self.__type_

    @property
    def difficulty(self):
        return self.__difficulty

    @property
    def weight(self):
        return self.__weight

    @property
    def question(self):
        return self.__question

    @property
    def options(self):
        return self.__options

    def __str__(self) -> str:
        options_str = ', '.join([f'({letter}) {text}' for letter, text in self.__options])
        return f'Unit: {self.__unit}\n' \
               f'Code: {self.__code}\n' \
               f'Time: {self.__time}\n' \
               f'Type: {self.__type_}\n' \
               f'Difficulty: {self.__difficulty}\n' \
               f'Weight: {self.__weight}\n' \
               f'Question: {self.__question}\n' \
               f'Options: {options_str}'

    def __repr__(self) -> str:
        return f'<Question: {self.__question}>'
