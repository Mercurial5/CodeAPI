from abc import ABC, abstractmethod


class Executor(ABC):
    """
    Base class for all executors.

    Executor - Something, that can run commands. Examples:
    > Shell (Local Machine)
    > Docker (Virtual Machine).
    """

    @abstractmethod
    def run(self, command: str): pass

    @abstractmethod
    def communicate(self, data: str): pass
