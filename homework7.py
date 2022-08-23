from abc import ABC, abstractmethod
import concurrent.futures
import logging
import queue
import threading
import time


class Command(ABC):
    @abstractmethod
    def Execute(self) -> None:
        pass


class CommandRegular(Command):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value
        logging.info("Regular command number #%s created", self.value)

    def Execute(self) -> None:
        logging.info("Regular command number #%s executed", self.value)


class CommandSoftStop(Command):
    def __init__(self) -> None:
        super().__init__()
        logging.info("Soft stop command created")

    def Execute(self) -> None:
        logging.info("Soft stop command executed")


class CommandHardStop(Command):
    def __init__(self) -> None:
        super().__init__()
        logging.info("Hard stop command created")

    def Execute(self) -> None:
        logging.info("Hard stop command executed")


def Produce(queue: queue.Queue, count: int, softStop: bool = False, hardStop: bool = False):
    logging.info("Produce started")
    halfCount = count / 2
    for i in range(int(halfCount)):
        queue.put(CommandRegular(i))
    if softStop:
        queue.put(CommandSoftStop())
    if hardStop:
        queue.put(CommandHardStop())
    for i in range(int(halfCount), count):
        queue.put(CommandRegular(i))
    logging.info("Produce finished")


def Consume(queue: queue.Queue[Command]):
    softStop = False
    hardStop = False
    logging.info("Consume started")
    while (not hardStop
        and (not softStop or not queue.empty())):
        command = queue.get()
        try:
            command.Execute()
        except:
            logging.info("Command exeption raised")
        if isinstance(command, CommandSoftStop):
            softStop = True
        if isinstance(command, CommandHardStop):
            hardStop = True
    logging.info("Consume finished")


def Start(queue: queue.Queue[Command]):
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(Consume, queue)
        executor.submit(Produce, queue, 20, True, False)
    logging.info("Finished")