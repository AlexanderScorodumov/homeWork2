from abc import ABC, abstractmethod
from unittest.mock import Mock
import numpy as np


class Movable(ABC):
    @abstractmethod
    def get_position(self) -> list[int]:
        pass

    @abstractmethod
    def get_velocity(self) -> list[int]:
        pass

    @abstractmethod
    def set_position(self, position: list[int])  -> list[int]:
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
    def set_direction(self, direction: int) -> int:
        pass


class Move:
    def __init__(self, movable: Movable) -> None:
        self.movable = movable

    def execute(self) -> list[int]:
        #position value checking
        position = self.movable.get_position()
        if len(position) != 2:
            raise Exception("Position not correct")

        #velocity value checking
        velocity = self.movable.get_velocity()
        if len(velocity) != 2:
            raise Exception("Velocity not correct")

        #new position calculation
        new_position = self.movable.set_position(np.ndarray.tolist(np.array(position) + np.array(velocity)))
        if len(new_position) != 2:
            raise Exception("New position not correct")

        return new_position


class Rotate:
    def __init__(self, rotable: Rotable) -> None:
        self.rotable = rotable

    def execute(self) -> int:
        #direction value checking
        direction = self.rotable.get_direction()
        if direction == None:
            raise Exception("Direction not correct")

        #angular velocity value checking
        angular_velocity = self.rotable.get_angular_velocity()
        if angular_velocity == None:
            raise Exception("Angular velocity not correct")

        #directions number value checking
        directions_number = self.rotable.get_directions_number()
        if directions_number == None:
            raise Exception("Directions number not correct")

        #new direction calculation
        new_direction = self.rotable.set_direction((direction + angular_velocity) % directions_number)
        if new_direction == None:
            raise Exception("New direction not correct")

        return new_direction