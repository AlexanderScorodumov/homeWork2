from importlib.util import set_loader
import unittest
from unittest.mock import Mock, patch
import homework7 as main
import concurrent.futures


class TestClass(unittest.TestCase):
    @patch.object(main.CommandRegular, 'Execute')
    def test_CommandSoftStop(self, commandRegular):
        commandQueue = main.queue.Queue()
        commandCount = 11
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(main.Consume, commandQueue)
            executor.submit(main.Produce, commandQueue, commandCount, True, False)
        assert commandRegular.call_count == commandCount

    @patch.object(main.CommandRegular, 'Execute')
    def test_CommandHardStop(self, commandRegular):
        commandQueue = main.queue.Queue()
        commandCount = 11
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(main.Consume, commandQueue)
            executor.submit(main.Produce, commandQueue,  commandCount, False, True)
        assert commandRegular.call_count == int(commandCount / 2)