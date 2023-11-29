from abc import ABC, abstractmethod


class SpelledTextBoxContract(ABC):
    @abstractmethod
    def get_suggestions(self, word: str) -> set[str]:
        pass

    @abstractmethod
    def register_suggestions(self, word: str, suggestions: set[str]) -> None:
        pass
