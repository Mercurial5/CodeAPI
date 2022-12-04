from abc import ABC, abstractmethod


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

    @abstractmethod
    def run(self) -> str: pass
