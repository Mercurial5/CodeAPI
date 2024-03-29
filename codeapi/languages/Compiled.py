from abc import abstractmethod

from codeapi.languages import Language


class Compiled(Language):
    """
    Compiler - class which is derived from Translator. All languages
    which need to compile before run should be inherited from this class.
    """

    name = None

    @abstractmethod
    def compile(self): pass
