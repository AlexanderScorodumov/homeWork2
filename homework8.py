from abc import ABC, abstractmethod
from queue import Queue
import queue
from time import sleep
from typing import Callable, Deque, Dict
import pika, sys, os
import json
from homework5 import IoC
import threading
from collections import deque
import numpy as np

lock = threading.RLock()

class Command(ABC):
    @abstractmethod
    def Execute(self) -> None:
        pass


class Movable(ABC):
    @abstractmethod
    def GetPosition(self) -> list[int]:
        pass

    @abstractmethod
    def GetVelocity(self) -> list[int]:
        pass

    @abstractmethod
    def SetPosition(self, position: list[int]):
        pass

    @abstractmethod
    def SetVelocity(self, velocity: list[int]):
        pass


class Move(Command):
    def __init__(self, movable: Movable) -> None:
        super().__init__()
        self.movable = movable

    def Execute(self):
        #position value checking
        position = self.movable.GetPosition()

        #velocity value checking
        velocity = self.movable.GetVelocity()

        #new position calculation
        self.movable.SetPosition(np.ndarray.tolist(np.array(position) + np.array(velocity)))


class ChangeVelocity(Command):
    def __init__(self, movable: Movable, velocity: list[int]) -> None:
        super().__init__()
        self.movable = movable
        self.newVelocity = velocity

    def Execute(self):
        self.movable.SetVelocity(self.newVelocity)


class ChangePosition(Command):
    def __init__(self, movable: Movable, position: list[int]) -> None:
        super().__init__()
        self.movable = movable
        self.newPosition = position

    def Execute(self):
        self.movable.SetPosition(self.newPosition)


class TestMovableObject(Movable):
    def __init__(self, position: list[int], velocity: list[int]) -> None:
        super().__init__()
        self.position = position
        self.velocity = velocity

    def GetPosition(self) -> list[int]:
        print("Get position = %s" % self.position)
        return self.position

    def GetVelocity(self) -> list[int]:
        print("Get velocity = %s" % self.velocity)
        return self.velocity

    def SetPosition(self, position: list[int]):
        self.position = position
        print("Set position = %s" % self.position)

    def SetVelocity(self, velocity: list[int]):
        self.velocity = velocity
        print("Set velocity = %s" % self.velocity)


class InterpretCommand(Command):
    def __init__(self, gameId: str, objectId: str, operationId: str, args: dict) -> None:
        super().__init__()
        self.gameId = gameId
        self.objectId = objectId
        self.operationId = operationId
        self.args = args

    def Execute(self) -> None:
        print("InterpretCommand from game #%s" % self.gameId)
        IoC.Resolve(Command, "Scopes.Current", str(self.gameId)).Execute()
        obj = IoC.Resolve(object, "Object", self.objectId)
        cmd = IoC.Resolve(Command, self.operationId, obj, self.args)
        IoC.Resolve(None, "GameQueue", cmd)


class CheckCommand(Command):
    def __init__(self, gameId: str, gameQueue: Deque[Command], eventQueue: Queue[Command]) -> None:
        super().__init__()
        self.gameId = gameId
        self.gameQueue = gameQueue
        self.eventQueue = eventQueue

    def Execute(self) -> None:
        if not self.eventQueue.empty():
            print("Check from game #%s" % self.gameId)
            self.eventQueue.get().Execute()
        self.gameQueue.append(self)


class GameCommand(Command):
    def __init__(self, gameId: str) -> None:
        super().__init__()
        self.gameId = gameId
        self.gameQueue: Deque[Command] = deque()
        self.eventQueue: Queue[Command] = Queue()
        self.scope: Dict[str, Callable] = dict()
        self.objects: Dict[str, object] = dict()
        #self.objects[1] = TestMovableObject(position=[1,1], velocity=[2,2])
        self.gameQueue.append(CheckCommand(gameId=self.gameId, gameQueue=self.gameQueue, eventQueue=self.eventQueue))
        with lock:
            IoC.Resolve(Command, "Scopes.New", self.gameId).Execute()
            IoC.Resolve(Command, "Scopes.Current", self.gameId).Execute()
            IoC.Resolve(Command, "IoC.Register", "GameQueue", lambda command: self.gameQueue.append(command)).Execute()
            IoC.Resolve(Command, "IoC.Register", "EventQueue", lambda command: self.eventQueue.put(command)).Execute()
            IoC.Resolve(Command, "IoC.Register", "Object", lambda objectId: self.objects[objectId]).Execute()
            IoC.Resolve(Command, "IoC.Register", "Move", lambda object, args: Move(movable=object)).Execute()
            IoC.Resolve(Command, "IoC.Register", "ChangeVelocity", lambda object, args: ChangeVelocity(movable=object, velocity=args)).Execute()
            IoC.Resolve(Command, "IoC.Register", "ChangePosition", lambda object, args: ChangePosition(movable=object, position=args)).Execute()
        print("New game #%s" % self.gameId)

    def Execute(self) -> None:
        while self.gameQueue:
            self.gameQueue.popleft().Execute()


class TestObject(object):
    def __init__(self, data) -> None:
        self.__dict__ = json.loads(data)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    testObject = TestObject(body)
    try:
        interpretCommand = InterpretCommand(gameId=testObject.gameId, objectId=testObject.objectId, operationId=testObject.operationId, args=testObject.args)
    except:
        raise AttributeError("%s - unsupported JSON format" % body)
    with lock:
        IoC.Resolve(Command, "Scopes.Current", str(testObject.gameId)).Execute()
        IoC.Resolve(None, "EventQueue", interpretCommand)


def GetMessage():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def GameFunction():
    game = GameCommand(gameId=threading.get_ident())
    game.Execute()
    

# if __name__ == '__main__':
#     rabbitThread = threading.Thread(target=GetMessage)
#     rabbitThread.start()
#     gameList: list[threading.Thread] = []
#     for i in range(5):
#         gameList.append(threading.Thread(target=GameFunction))
#     for i in range(5):
#         gameList[i].start()    