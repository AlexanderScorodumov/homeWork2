import unittest
from unittest.mock import Mock
import homework2


class TestMovable(unittest.TestCase):
    def test_set_position(self):
        movable_mock = Mock()
        movable_mock.get_position.return_value = [12, 5]
        movable_mock.get_velocity.return_value = [-7, 3]      
        move = homework2.Move(movable_mock)
        move.execute()
        movable_mock.set_position.assert_called_with([5, 8])
    
    def test_get_position_exception(self):
        movable_mock = Mock()
        movable_mock.get_position.side_effect = Exception()
        movable_mock.get_velocity.return_value = [-7, 3]
        move = homework2.Move(movable_mock)
        self.assertRaises(Exception, move.execute)

    def test_get_velocity_exception(self):
        movable_mock = Mock()
        movable_mock.get_position.return_value = [12, 5]
        movable_mock.get_velocity.side_effect = Exception()
        move = homework2.Move(movable_mock)
        self.assertRaises(Exception, move.execute)

    def test_set_position_exception(self):
        movable_mock = Mock()
        movable_mock.set_position.side_effect = Exception()
        move = homework2.Move(movable_mock)
        self.assertRaises(Exception, move.execute)
        

class TestRotable(unittest.TestCase):
    def test_set_direction(self):
        rotable_mock = Mock()
        rotable_mock.get_direction.return_value = 5
        rotable_mock.get_angular_velocity.return_value = 11
        rotable_mock.get_directions_number.return_value = 360
        rotate = homework2.Rotate(rotable_mock)
        rotate.execute()
        rotable_mock.set_direction.assert_called_with(16)

    def test_get_direction_exception(self):
        rotable_mock = Mock()
        rotable_mock.get_direction.side_effect = Exception()
        rotable_mock.get_angular_velocity.return_value = 11
        rotable_mock.get_directions_number.return_value = 360
        rotate = homework2.Rotate(rotable_mock)
        self.assertRaises(Exception, rotate.execute)
            

    def test_get_angular_velocity_exception(self):
        rotable_mock = Mock()
        rotable_mock.get_direction.return_value = 5
        rotable_mock.get_angular_velocity.side_effect = Exception()
        rotable_mock.get_directions_number.return_value = 360
        rotate = homework2.Rotate(rotable_mock)
        rotate = homework2.Rotate(rotable_mock)
        self.assertRaises(Exception, rotate.execute)

    def test_get_directions_number_exception(self):
        rotable_mock = Mock()
        rotable_mock.get_direction.return_value = 5
        rotable_mock.get_angular_velocity.return_value = 11
        rotable_mock.get_directions_number.side_effect = Exception()
        rotate = homework2.Rotate(rotable_mock)
        self.assertRaises(Exception, rotate.execute)

    def test_set_direction_exception(self):
        rotable_mock = Mock()
        rotable_mock.set_direction.side_effect = Exception()
        rotate = homework2.Rotate(rotable_mock)
        rotate = homework2.Rotate(rotable_mock)
        self.assertRaises(Exception, rotate.execute)