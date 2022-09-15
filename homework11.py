from __future__ import annotations
from abc import ABC, abstractmethod
from collections import deque
from typing import Deque
import logging


class Command(ABC):
    @abstractmethod
    def Execute(self) -> None:
        pass


class State(ABC):
    @abstractmethod
    def Handle(self) -> State:
        pass


class CommandRegular(Command):
    def __init__(self, value=0) -> None:
        super().__init__()
        self.value = value
        logging.info("Regular command number #%s created", self.value)

    def Execute(self) -> None:
        logging.info("Regular command number #%s executed", self.value)


class CommandHardStop(Command):
    def __init__(self) -> None:
        super().__init__()
        logging.info("Hard stop command created")

    def Execute(self) -> None:
        logging.info("Hard stop command executed")


class CommandRun(Command):
    def __init__(self) -> None:
        super().__init__()
        logging.info("Run command created")

    def Execute(self) -> None:
        logging.info("Run command executed")


class CommandMoveTo(Command):
    def __init__(self) -> None:
        super().__init__()
        logging.info("Move to command created")

    def Execute(self) -> None:
        logging.info("Move to command executed")


class StateMoveTo(State):
    def __init__(self, deque: Deque[Command], stateNormal: State) -> None:
        super().__init__()
        self.deque = deque
        self.stateNormal = stateNormal

    def Handle(self) -> State:
        command = self.deque.popleft()
        try:
            logging.info("Command execution from state MoveTo, id=%s" % id(self))
            command.Execute()            
        except:
            logging.info("Command exeption raised")
        if isinstance(command, CommandHardStop):
            return None
        if isinstance(command, CommandRun):
            return self.stateNormal
        return self


class StateNormal(State):
    def __init__(self, deque: Deque[Command]) -> None:
        super().__init__()
        self.deque = deque
        self.stateMoveTo = StateMoveTo(deque=self.deque, stateNormal=self)

    def Handle(self) -> State:
        command = self.deque.popleft()
        try:
            logging.info("Command execution from state Normal, id=%s" % id(self))
            command.Execute()      
        except:
            logging.info("Command exeption raised")
        if isinstance(command, CommandHardStop):
            return None
        if isinstance(command, CommandMoveTo):
            return self.stateMoveTo
        return self


class GameCommand(Command):
    def __init__(self) -> None:
        super().__init__()
        self.gameQueue: Deque[Command] = deque()
        self.state = StateNormal(deque=self.gameQueue)

    def Execute(self) -> None:
        while self.state:
            self.state = self.state.Handle()


if __name__ == '__main__':
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    game = GameCommand()
    game.gameQueue.append(CommandRegular(1))
    game.gameQueue.append(CommandMoveTo())
    game.gameQueue.append(CommandRegular(2))
    game.gameQueue.append(CommandRun())
    game.gameQueue.append(CommandRegular(3))
    game.gameQueue.append(CommandMoveTo())
    game.gameQueue.append(CommandRegular(4))
    game.gameQueue.append(CommandRun())
    game.gameQueue.append(CommandRegular(5))
    game.gameQueue.append(CommandMoveTo())
    game.gameQueue.append(CommandRegular(6))
    game.gameQueue.append(CommandHardStop())
    game.Execute()
    logging.info("Finished")