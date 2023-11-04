from pathlib import Path

from spellchecker import SpellChecker

from src.Contracts.speller import SpellerContract


class PySpellChecker(SpellChecker, SpellerContract):
    def __init__(self, local_dictionary: Path):
        super().__init__(local_dictionary=str(local_dictionary), case_sensitive=True)

    def tokenize_words(self, text: str) -> set[str]:
        return set(self.split_words(text))

    def check_spelling(self, words_list: set[str]) -> set[str]:
        return self.unknown(words_list)

    def suggest_corrections(self, word: str) -> set[str]:
        return self.candidates(word)
