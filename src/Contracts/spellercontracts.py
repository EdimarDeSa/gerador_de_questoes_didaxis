from abc import ABC, abstractmethod


class SpellerContract(ABC):
    @abstractmethod
    def tokenize_words(self, text: str) -> set[str]:
        pass

    @abstractmethod
    def check_spelling(self, words_list: set[str]) -> set[str]:
        pass

    @abstractmethod
    def suggest_corrections(self, word: str) -> set[str]:
        pass

    @abstractmethod
    def export_word_usage(self) -> None:
        pass

    @abstractmethod
    def add_new_word(self, word: str) -> None:
        pass
