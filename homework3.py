from abc import ABC, abstractmethod
import numpy as np
import homework2
from unittest.mock import Mock

class Fuel(ABC):
    @abstractmethod
    def get_fuel(self):
        pass

    @abstractmethod
    def get_fuel_flow(self) -> int:
        pass

    @abstractmethod
    def set_fuel(value: int):
        pass
    

class VelocityChangable(homework2.Movable, homework2.Rotable):
    @abstractmethod
    def set_velocity(self, velocity: list[int]):
        pass


class CheckFuelCommand(homework2.Command):
    def __init__(self, fuel: Fuel) -> None:
        super().__init__()
        self.fuel = fuel

    def execute(self):
        fuel = self.fuel.get_fuel()
        fuel_flow = self.fuel.get_fuel_flow()
        if (fuel < 0
                or fuel_flow < 0
                or fuel < fuel_flow):
            raise Exception()


class BurnFuelCommand(homework2.Command):
    def __init__(self, fuel: Fuel) -> None:
        super().__init__()
        self.fuel = fuel

    def execute(self):
        fuel = self.fuel.get_fuel() - self.fuel.get_fuel_flow()
        if fuel < 0:
            raise Exception()
        self.fuel.set_fuel(fuel)


class ChangeVelocityCommand(homework2.Command):
    def __init__(self, velocity_changable: VelocityChangable) -> None:
        super().__init__()
        self.velocity_changable = velocity_changable

    def execute(self):
        angular_velocity = self.velocity_changable.get_angular_velocity()
        directions_number = self.velocity_changable.get_directions_number()
        angle = (angular_velocity / directions_number) * 2 * np.pi
        velocity = self.velocity_changable.get_velocity()
        new_velocity_x = round(velocity[0] * np.cos(angle) - velocity[1] * np.sin(angle))
        new_velocity_y = round(velocity[1] * np.cos(angle) + velocity[0] * np.sin(angle))
        self.velocity_changable.set_velocity([new_velocity_x, new_velocity_y])


class MacroCommand(homework2.Command):
    def __init__(self, commands: list[homework2.Command]) -> None:
        super().__init__()
        self.commands = commands

    def execute(self):
        for command in self.commands:
            command.execute()