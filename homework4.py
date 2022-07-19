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
        print("Log command")
        pass


class RepeaterCommand(Command):
    def __init__(self, command: Command) -> None:
        super().__init__()
        self.command = command

    def execute(self):
        #print("Repeater command")
        self.command.execute()


class DoubleRepeaterCommand(Command):
    def __init__(self, command: Command) -> None:
        super().__init__()
        self.command = RepeaterCommand(command)

    def execute(self):
        #print("Double repeater command")
        self.command.execute()


class ExceptionHandlerLogger(ExceptionHandler):
    def __init__(self, command_queue: list[Command]) -> None:
        super().__init__()
        self.command_queue = command_queue

    def handle(self, command: Command, exception: Exception):
        self.command_queue.append(LogCommand(exception))


class ExceptionHandlerRepeater(ExceptionHandler):
    def __init__(self, command_queue: list[Command]) -> None:
        super().__init__()
        self.command_queue = command_queue

    def handle(self, command: Command, exception: Exception):
        self.command_queue.append(RepeaterCommand(command))


class ExceptionHandlerDoubleRepeater(ExceptionHandler):
    def __init__(self, command_queue: list[Command]) -> None:
        super().__init__()
        self.command_queue = command_queue

    def handle(self, command: Command, exception: Exception):
        self.command_queue.append(DoubleRepeaterCommand(command))


class MainCommand(Command):
    def __init__(self, command_queue: list[Command], dictionary: dict[str, ExceptionHandler]) -> None:
        self.command_queue = command_queue
        self.dictionary = dictionary

    def execute(self):
        while(True):
            if len(self.command_queue) == 0:
                break

            command = self.command_queue.pop(0)
            try:
                command.execute()
            except Exception as ex:
                self.dictionary[command.__class__](self.command_queue).handle(command, ex)