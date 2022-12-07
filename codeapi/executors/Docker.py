from subprocess import Popen, PIPE, TimeoutExpired
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

        process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        self.container_id = process.stdout.read().decode('utf-8').strip()

        if process.stderr.read().decode('utf-8').strip():
            raise SystemError('Docker Issue')

        self.current_process: Popen | None = None

    def run(self, cmd: str):
        command = f'docker exec -i {self.container_id} {cmd}'
        self.current_process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)

    def communicate(self, data: str, timeout: int = 2) -> tuple:
        if self.current_process is None:
            raise ValueError('No process is currently running')

        try:
            response = self.current_process.communicate(data.encode('utf-8'), timeout)
        except TimeoutExpired:
            response = ''.encode('utf-8'), 'Timeout'.encode('utf-8')

        self.__kill_current_process()
        return response[0].decode('utf-8').strip(), response[1].decode('utf-8').strip()

    def __kill_current_process(self):
        filename = str(self.current_process.args.split()[5])
        command = f'docker exec -i {self.container_id} sh -c "ps ax|grep {filename}"'
        process = Popen(command, shell=True, stdout=PIPE)

        process_list = [process.split() for process in process.stdout.read().decode('utf-8').split('\n')]
        pid = next((process[0] for process in process_list if ' '.join(process[4:6]) == f'python {filename}'), None)

        if pid is None:
            return

        command = f'docker exec -i {self.container_id} kill {pid}'
        Popen(command, shell=True)

        self.current_process = None

    def __del__(self):
        command = f'docker rm -f {self.container_id}'
        Popen(command, shell=True)
