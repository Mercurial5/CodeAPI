from subprocess import Popen, PIPE
import os

from codeapi.executors import Executor


class Docker(Executor):
    """
    Class that manages docker to run commands.
    """

    def __init__(self, image: str):
        self.path_to_host_volume = os.getenv('PATH_TO_HOST_VOLUME')
        self.path_to_container_volume = os.getenv('PATH_TO_CONTAINER_VOLUME')

        command = f'docker run -i -dv {self.path_to_host_volume}:{self.path_to_container_volume}:ro {image}'

        process = Popen(command, shell=True, stdout=PIPE)
        self.container_id = process.stdout.read().decode('utf-8').strip()

        self.current_process: Popen | None = None

    def run(self, cmd: str):
        command = f'docker exec -i {self.container_id} {cmd}'
        self.current_process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)

    def communicate(self, data: str) -> tuple:
        if self.current_process is None:
            raise ValueError('No process is currently running')

        response = self.current_process.communicate(data.encode('utf-8'))

        return response

    def __del__(self):
        command = f'docker rm -f {self.container_id}'
        Popen(command, shell=True)
