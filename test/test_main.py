import unittest
from unittest.mock import Mock
import main


class TestMovable(unittest.TestCase):
    def test_set_position(self):
        movable_mock = Mock()
        attrs = {'get_position.return_value': [12, 5], 'get_velocity.return_value': [-7, 3], 'set_position.return_value': [5, 8]}
        movable_mock.configure_mock(**attrs)
        move = main.Move(movable_mock)
        result = move.execute()
        expected_result = [5, 8]
        self.assertListEqual(expected_result, result)

    def test_get_position_exception(self):
        movable_mock = Mock()
        attrs = {'get_position.return_value': [], 'get_velocity.return_value': [-7, 3], 'set_position.return_value': [5, 8]}
        movable_mock.configure_mock(**attrs)
        move = main.Move(movable_mock)
        with self.assertRaises(Exception):
            move.execute()

    def test_get_velocity_exception(self):
        movable_mock = Mock()
        attrs = {'get_position.return_value': [12, 5], 'get_velocity.return_value': [], 'set_position.return_value': [5, 8]}
        movable_mock.configure_mock(**attrs)
        move = main.Move(movable_mock)
        with self.assertRaises(Exception):
            move.execute()

    def test_set_position_exception(self):
        movable_mock = Mock()
        attrs = {'get_position.return_value': [12, 5], 'get_velocity.return_value': [-7, 3], 'set_position.return_value': []}
        movable_mock.configure_mock(**attrs)
        move = main.Move(movable_mock)
        with self.assertRaises(Exception):
            move.execute()
        

class TestRotable(unittest.TestCase):
    def test_set_direction(self):
        rotable_mock = Mock()
        attrs = {'get_direction.return_value': 5, 'get_angular_velocity.return_value': 11, 'get_directions_number.return_value': 360, 'set_direction.return_value': 16}
        rotable_mock.configure_mock(**attrs)
        rotate = main.Rotate(rotable_mock)
        result = rotate.execute()
        expected_result = 16
        self.assertEqual(expected_result, result)

    def test_get_direction_exception(self):
        rotable_mock = Mock()
        attrs = {'get_direction.return_value': None, 'get_angular_velocity.return_value': 11, 'get_directions_number.return_value': 360, 'set_direction.return_value': 16}
        rotable_mock.configure_mock(**attrs)
        rotate = main.Rotate(rotable_mock)
        with self.assertRaises(Exception):
            rotate.execute()

    def test_get_angular_velocity_exception(self):
        rotable_mock = Mock()
        attrs = {'get_direction.return_value': 5, 'get_angular_velocity.return_value': None, 'get_directions_number.return_value': 360, 'set_direction.return_value': 16}
        rotable_mock.configure_mock(**attrs)
        rotate = main.Rotate(rotable_mock)
        with self.assertRaises(Exception):
            rotate.execute()

    def test_get_directions_number_exception(self):
        rotable_mock = Mock()
        attrs = {'get_direction.return_value': 5, 'get_angular_velocity.return_value': 11, 'get_directions_number.return_value': None, 'set_direction.return_value': 16}
        rotable_mock.configure_mock(**attrs)
        rotate = main.Rotate(rotable_mock)
        with self.assertRaises(Exception):
            rotate.execute()

    def test_set_direction_exception(self):
        rotable_mock = Mock()
        attrs = {'get_direction.return_value': 5, 'get_angular_velocity.return_value': 11, 'get_directions_number.return_value': 360, 'set_direction.return_value': None}
        rotable_mock.configure_mock(**attrs)
        rotate = main.Rotate(rotable_mock)
        with self.assertRaises(Exception):
            rotate.execute()