from uuid import uuid4
import os


class FileManager:
    """
    Works with files.
    """

    def __init__(self, base_path: str):
        if not os.path.exists(base_path):
            raise ValueError(f"Path {base_path} does not exists")

        self.base_path = base_path

    def create(self, content: str, filename: str = None, extension: str = None) -> str:
        filename = self.__generate_random_filename() if filename is None else filename
        filename += extension if extension else ''

        path_to_file = os.path.join(self.base_path, filename)

        if os.path.exists(path_to_file):
            raise ValueError(f"File {path_to_file} already exists")

        with open(path_to_file, 'w') as file:
            file.write(content)

        return filename

    def delete(self, filename: str):
        path_to_file = os.path.join(self.base_path, filename)
        if not os.path.exists(path_to_file):
            raise ValueError(f"File {path_to_file} does not exists")

        os.remove(path_to_file)

    @staticmethod
    def __generate_random_filename():
        return uuid4().hex
