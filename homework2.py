from abc import ABC, abstractmethod
import numpy as np


class Movable(ABC):
    @abstractmethod
    def get_position(self) -> list[int]:
        pass

    @abstractmethod
    def get_velocity(self) -> list[int]:
        pass

    @abstractmethod
    def set_position(self, position: list[int]):
        pass


class Rotable(ABC):
    @abstractmethod
    def get_direction(self) -> int:
        pass

    @abstractmethod
    def get_angular_velocity(self) -> int:
        pass

    @abstractmethod
    def get_directions_number(self) -> int:
        pass

    @abstractmethod
    def set_direction(self, direction: int):
        pass


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class Move(Command):
    def __init__(self, movable: Movable) -> None:
        super().__init__()
        self.movable = movable

    def execute(self):
        #position value checking
        position = self.movable.get_position()

        #velocity value checking
        velocity = self.movable.get_velocity()

        #new position calculation
        self.movable.set_position(np.ndarray.tolist(np.array(position) + np.array(velocity)))


class Rotate(Command):
    def __init__(self, rotable: Rotable) -> None:
        super().__init__()
        self.rotable = rotable

    def execute(self):
        #direction value checking
        direction = self.rotable.get_direction()

        #angular velocity value checking
        angular_velocity = self.rotable.get_angular_velocity()

        #directions number value checking
        directions_number = self.rotable.get_directions_number()

        #new direction calculation
        self.rotable.set_direction((direction + angular_velocity) % directions_number)

