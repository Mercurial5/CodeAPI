from uuid import uuid4
import shutil
import os


class FileManager:
    """
    Works with files.
    """

    def __init__(self, base_path: str):
        if not os.path.exists(base_path):
            raise ValueError(f'Path {base_path} does not exists')

        self.base_path = base_path

    def create_file(self, content: str, filename: str = None, extension: str = None) -> str:
        filename = self.__generate_random_name() if filename is None else filename
        filename += extension if extension else ''

        path_to_file = os.path.join(self.base_path, filename)

        if os.path.exists(path_to_file):
            raise ValueError(f'File {path_to_file} already exists')

        with open(path_to_file, 'w') as file:
            file.write(content)

        return filename

    def create_directory(self, dirname: str) -> str:
        path_to_dir = os.path.join(self.base_path, dirname)
        if os.path.exists(path_to_dir):
            raise ValueError(f'Directory {path_to_dir} already exists')

        os.mkdir(path_to_dir)
        return dirname

    def delete_file(self, filename: str):
        path_to_file = os.path.join(self.base_path, filename)
        if not os.path.exists(path_to_file):
            raise ValueError(f'File {path_to_file} does not exists')

        os.remove(path_to_file)

    def delete_directory(self, dirname: str):
        path_to_dir = os.path.join(self.base_path, dirname)
        if not os.path.exists(path_to_dir):
            raise ValueError(f'Directory {path_to_dir} does not exists')

        shutil.rmtree(path_to_dir)

    def is_directory_exists(self, dirname: str):
        path_to_dir = os.path.join(self.base_path, dirname)
        return os.path.exists(path_to_dir)

    @staticmethod
    def join(*paths):
        return os.path.join(*paths)

    @staticmethod
    def __generate_random_name():
        return uuid4().hex
