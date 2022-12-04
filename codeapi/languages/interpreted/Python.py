from codeapi.languages import Interpreted
from codeapi.utils import FileManager


class Python(Interpreted):
    name = 'python'
    extension = '.py'

    def __init__(self):
        super().__init__()

        file_manager = FileManager(self.languages_path)
        if not file_manager.is_directory_exists(self.name):
            file_manager.create_directory(self.name)

        self.path = file_manager.join(self.languages_path, self.name)

    def run(self, filename: str) -> str:
        return f'python {filename}'
