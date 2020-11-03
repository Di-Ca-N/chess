import abc


class Command(abc.ABC):
    @abc.abstractmethod
    def do(self, board):
        raise NotImplementedError

    @abc.abstractmethod
    def undo(self, board):
        raise NotImplementedError
