from codeapi.languages import Language


class Interpreted(Language):
    """
    Interpreter - class which is derived from Translator. All languages
    which does not need to compile before run should be inherited from this class.
    """

    name = None
