from __future__ import annotations

from abc import ABC, abstractmethod
import os


class Language(ABC):
    """
    Language - base class which represents all the languages.
    Each language can be divided into compiler and interpreter based.

    All languages have their own separate directory, where their code is
    being executed.

    All languages have property `name` which is super-property. It's used for:
    > Name of the separate language directory.
    > Finding class of the language by name.
    """

    # path to the separate directory of language
    path = None
    name = None
    extension = None

    def __init__(self):
        self.languages_path = os.getenv('LANGUAGES_PATH')

    @abstractmethod
    def run(self, filename: str) -> str: pass

    @staticmethod
    def get_language_by_name(name: str) -> Language:
        languages = [language for language_type in Language.__subclasses__() for language in
                     language_type.__subclasses__()]
        language = next((language for language in languages if language.name == name), None)

        if language is None:
            raise ValueError(f'No such language as {name}')

        return language()
