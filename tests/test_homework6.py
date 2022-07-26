import unittest
from unittest.mock import Mock, patch
import homework6 as main


class TestClass(unittest.TestCase):
    def setUp(self):
        #Set up mock
        self.objMock = Mock(main.ObjectProperty)
        #Generate adapter from IoC
        main.IoC.Resolve(main.Command, "IoC.Register", "Adapter", main.GenerateAdapter)
        self.generatedAdapter = main.IoC.Resolve(main.Movable, "Adapter", main.Movable, self.objMock)
    

    def tearDown(self):
        pass


    def test_GetPositionCallFromAdapter(self):
        self.generatedAdapter.GetPosition()
        self.objMock.GetProperty.assert_called_with("Position")


    def test_GetVelocityCallFromAdapter(self):
        self.generatedAdapter.GetVelocity()
        self.objMock.GetProperty.assert_called_with("Velocity")
        

    def test_SetPositionCallFromAdapter(self):
        newPosition = [1, 1]
        self.generatedAdapter.SetPosition(newPosition)
        self.objMock.SetProperty.assert_called_with("Position", newPosition)
    