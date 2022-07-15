from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class ExceptionHandler(ABC):
    @abstractmethod
    def handle(self, command: Command, exception: Exception):
        pass


class LogCommand(Command):
    def __init__(self, exception: Exception) -> None:
        super().__init__()
        self.exception = exception
        

    def execute(self):
        pass


class RepeaterCommand(Command):
    def __init__(self, command: Command) -> None:
        super().__init__()
        self.command = command

    def execute(self):
        print("Repeater")
        self.command.execute()


class DoubleRepeaterCommand(Command):
    def __init__(self, command: Command) -> None:
        super().__init__()
        self.command = RepeaterCommand(command)

    def execute(self):
        print("DoubleRepeater")
        self.command.execute()


class ExceptionHandlerLogger():
    def __init__(self, commandList: list[Command]) -> None:
        self.commandList = commandList

    def handle(self, command: Command, exception: Exception):
        self.commandList.append(LogCommand(exception))


class ExceptionHandlerRepeater():
    def __init__(self, commandList: list[Command]) -> None:
        self.commandList = commandList

    def handle(self, command: Command, exception: Exception):
        if not(isinstance(command, RepeaterCommand)):
            self.commandList.append(RepeaterCommand(command))


class ExceptionHandlerRepeaterAndLogger():
    def __init__(self, commandList: list[Command]) -> None:
        self.commandList = commandList

    def handle(self, command: Command, exception: Exception):
        if not (isinstance(command, RepeaterCommand)):
            self.commandList.append(RepeaterCommand(command))
        else:
            self.commandList.append(LogCommand(exception))


class ExceptionHandlerDoubleRepeaterAndLogger():
    def __init__(self, commandList: list[Command]) -> None:
        self.commandList = commandList

    def handle(self, command: Command, exception: Exception):
        if not(isinstance(command, RepeaterCommand)):
            if not (isinstance(command, DoubleRepeaterCommand)):
                self.commandList.append(DoubleRepeaterCommand(command))
            else:
                self.commandList.append(RepeaterCommand(command))
        else:
            self.commandList.append(LogCommand(exception))
        

class MainCommand(Command):
    def __init__(self, commandQueue: list[Command], exceptionHandler: ExceptionHandler) -> None:
        super().__init__()
        self.commandQueue = commandQueue
        self.exceptionHandler = exceptionHandler

    def execute(self):
        while(True):
            if len(self.commandQueue) == 0:
                break

            command = self.commandQueue.pop(0)
            try:
                command.execute()
            except Exception as ex:
                self.exceptionHandler.handle(command, ex)