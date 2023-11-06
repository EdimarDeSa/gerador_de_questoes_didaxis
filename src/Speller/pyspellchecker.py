from pathlib import Path
from functools import lru_cache, cache

from spellchecker import SpellChecker

from src.Contracts.speller import SpellerContract


class PySpellChecker(SpellChecker, SpellerContract):
    def __init__(self, local_dictionary: Path):
        self.local_dictionary = str(local_dictionary)

        super().__init__(
            local_dictionary=self.local_dictionary, case_sensitive=True
        )

    @lru_cache(maxsize=100, typed=False)
    def tokenize_words(self, text: str) -> set[str]:
        return set([word for word in self.split_words(text) if not word.isupper()])

    def check_spelling(self, words_list: set[str]) -> set[str]:
        return self.unknown(words_list)

    @lru_cache(maxsize=100, typed=False)
    def suggest_corrections(self, word: str) -> set[str]:
        return self.candidates(word)

    def export_word_usage(self) -> None:
        self.export(self.local_dictionary, gzipped=False)

    def add_new_word(self, word: str) -> None:
        self._word_frequency.add(word)
        self.export_word_usage()
