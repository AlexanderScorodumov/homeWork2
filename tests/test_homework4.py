import unittest
from unittest.mock import Mock, patch
import homework4 as source


class TestExceptionHandlers(unittest.TestCase):
    def setUp(self):      
        #Mocks creation
        self.count = 10
        self.mocks = []
        self.commands_queue = []
        for i in range(self.count):
            self.mocks.append(Mock())
            self.mocks[i].execute.side_effect = Exception()
            self.commands_queue.append(self.mocks[i])                 

    
    def tearDown(self):
        self.mocks.clear()
        self.commands_queue.clear()


    @patch.object(source.LogCommand, 'execute')
    def test_handler_logger(self, mock_log_command_execute):
        mock_log_command_execute.return_value = True
 
        #Main command execute
        main_command = source.MainCommand(self.commands_queue, source.ExceptionHandlerLogger(self.commands_queue))
        main_command.execute()

        #Asserts
        for i in range(self.count):
            assert self.mocks[i].execute.call_count == 1
        assert mock_log_command_execute.call_count == self.count

    @patch.object(source.LogCommand, 'execute')
    def test_handler_repeater(self, mock_log_command_execute):
        mock_log_command_execute.return_value = True
 
        #Main command execute
        main_command = source.MainCommand(self.commands_queue, source.ExceptionHandlerRepeater(self.commands_queue))
        main_command.execute()

        #Asserts
        for i in range(self.count):
            assert self.mocks[i].execute.call_count == 2
        assert mock_log_command_execute.call_count == 0


    @patch.object(source.LogCommand, 'execute')
    def test_handler_repeater_and_logger(self, mock_log_command_execute):
        mock_log_command_execute.return_value = True
 
        #Main command execute
        main_command = source.MainCommand(self.commands_queue, source.ExceptionHandlerRepeaterAndLogger(self.commands_queue))
        main_command.execute()

        #Asserts
        for i in range(self.count):
            assert self.mocks[i].execute.call_count == 2
        assert mock_log_command_execute.call_count == self.count

    @patch.object(source.LogCommand, 'execute')
    def test_handler_double_repeater_and_logger(self, mock_log_command_execute):
        mock_log_command_execute.return_value = True
 
        #Main command execute
        main_command = source.MainCommand(self.commands_queue, source.ExceptionHandlerDoubleRepeaterAndLogger(self.commands_queue))
        main_command.execute()

        #Asserts
        for i in range(self.count):
            assert self.mocks[i].execute.call_count == 3
        assert mock_log_command_execute.call_count == self.count