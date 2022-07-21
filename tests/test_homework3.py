import unittest
from unittest.mock import Mock
from parameterized import parameterized
import homework3, homework2


class TestCheckFuelCommand(unittest.TestCase):
    @parameterized.expand([
        #exception, fuel, fuel_flow
        (False, 15 ,5),
        (False, 0 ,0),
        (True, 2 ,4),
        (True, -1, 5),
        (True, 5 ,-1),
    ])
    def test_get_fuel(self, exception, fuel, fuel_flow):
        fuel_mock = Mock()
        fuel_mock.get_fuel.return_value = fuel
        fuel_mock.get_fuel_flow.return_value = fuel_flow      
        check_fuel_command = homework3.CheckFuelCommand(fuel_mock)
        if exception:
            self.assertRaises(Exception, check_fuel_command.execute)
        else:
            check_fuel_command.execute()


class TestBurnFuelCommand(unittest.TestCase):
    @parameterized.expand([
        #exception, fuel, fuel_flow, result
        (False, 15 ,5, 10),
        (False, 1 ,1, 0),
        (False, 0 ,0, 0),
        (True, 2 ,4, 0),
        (True, -1 ,5, 0),
        (False, 5 ,-1, 6),
    ])
    def test_get_fuel(self, exception, fuel, fuel_flow, result):
        fuel_mock = Mock()
        fuel_mock.get_fuel.return_value = fuel
        fuel_mock.get_fuel_flow.return_value = fuel_flow      
        burn_fuel_command = homework3.BurnFuelCommand(fuel_mock)
        if exception:
            self.assertRaises(Exception, burn_fuel_command.execute)
        else:
            burn_fuel_command.execute()
            fuel_mock.set_fuel.assert_called_with(result)


class TestMacroCommand(unittest.TestCase):
    @parameterized.expand([
        #exception, count
        (False, 0),
        (False, 5),
    ])
    def test_execute(self, exception, count):
        command_list_mock = []
        for i in range(count): 
            command_list_mock.append(Mock())
        macrocommand = homework3.MacroCommand(command_list_mock)
        if exception:
            self.assertRaises(Exception, macrocommand.execute)
        else:
            macrocommand.execute()
        for i in range(count):
            command_list_mock[i].execute.assert_called_once()


class TestCheckMoveAndBurnFuelMacroCommand(unittest.TestCase):
    @parameterized.expand([
        #exception, position, velocity, fuel, fuel_flow, result_position, result_fuel
        (False, [12, 5] ,[-7, 3], 15, 5, [5, 8], 10),
        (False, [12, 5] ,[0, 0], 10, 2, [12, 5], 8),
        (False, [-12, -5] ,[7, 3], 15, 0, [-5, -2], 15),
        (True, [-12, -5] ,[7, 3], -15, 5, [-5, -2], 0),
        (True, [-12, -5] ,[7, 3], 15, -5, [-5, -2], 0),
    ])
    def test_execute(self, exception, position, velocity, fuel, fuel_flow, result_position, result_fuel):
        fuel_movable_mock = Mock()
        fuel_movable_mock.get_position.return_value = position
        fuel_movable_mock.get_velocity.return_value = velocity
        fuel_movable_mock.get_fuel.return_value = fuel
        fuel_movable_mock.get_fuel_flow.return_value = fuel_flow    
        macrocommand = homework3.MacroCommand([
            homework3.CheckFuelCommand(fuel_movable_mock),
            homework2.Move(fuel_movable_mock),
            homework3.BurnFuelCommand(fuel_movable_mock)
        ])
        if exception:
            self.assertRaises(Exception, macrocommand.execute)
        else:
            macrocommand.execute()
            fuel_movable_mock.set_position.assert_called_with(result_position)
            fuel_movable_mock.set_fuel.assert_called_with(result_fuel)


class TestChangeVelocity(unittest.TestCase):
    @parameterized.expand([
        #exception, angular_velocity, directions_number, velocity, result_velocity
        (False, 180, 360, [2, 2], [-2, -2]),
        (False, -180, 360, [2, 2], [-2, -2]),
        (False, 90, 360, [2, 2], [-2, 2]),
        (False, -90, 360, [2, 2], [2, -2]),
        (False, 0, 360, [2, 2], [2, 2]),
        (False, 360, 360, [2, 2], [2, 2]),
        (False, -720, 360, [2, 2], [2, 2]),
    ])
    def test_execute(self, exception, angular_velocity, directions_number, velocity, result_velocity):
        velocity_changable_mock = Mock()
        velocity_changable_mock.get_angular_velocity.return_value = angular_velocity
        velocity_changable_mock.get_directions_number.return_value = directions_number
        velocity_changable_mock.get_velocity.return_value = velocity
        change_velocity_command = homework3.ChangeVelocityCommand(velocity_changable_mock)
        if exception:
            self.assertRaises(Exception, change_velocity_command.execute)
        else:
            change_velocity_command.execute()
            velocity_changable_mock.set_velocity.assert_called_with(result_velocity)


class TestRotateAndChangeVelocityCommand(unittest.TestCase):
    @parameterized.expand([
        #exception, velocity, direction, angular_velocity, directions_number, result_direction, result_velocity
        (False, [2, 2] , 5, 90, 360, 95, [-2, 2]),
        (False, [2, 2] , 25, 180, 360, 205, [-2, -2]),
        (False, [2, 2] , 25, 0, 360, 25, [2, 2]),
        (False, [0, 0] , 25, 270, 360, 295, [0, 0]),
    ])
    def test_execute(self, exception, velocity, direction, angular_velocity, directions_number, result_direction, result_velocity):
        rotable_velocity_changable_mock = Mock()
        rotable_velocity_changable_mock.get_velocity.return_value = velocity
        rotable_velocity_changable_mock.get_direction.return_value = direction
        rotable_velocity_changable_mock.get_angular_velocity.return_value = angular_velocity
        rotable_velocity_changable_mock.get_directions_number.return_value = directions_number
        macrocommand = homework3.MacroCommand([
            homework2.Rotate(rotable_velocity_changable_mock),
            homework3.ChangeVelocityCommand(rotable_velocity_changable_mock)
        ])
        if exception:
            self.assertRaises(Exception, macrocommand.execute)
        else:
            macrocommand.execute()
            rotable_velocity_changable_mock.set_direction.assert_called_with(result_direction)
            rotable_velocity_changable_mock.set_velocity.assert_called_with(result_velocity)