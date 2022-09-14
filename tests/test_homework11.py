import unittest
from unittest.mock import patch
import homework11 as main

@patch.object(main.CommandRegular, "Execute")
@patch.object(main.CommandHardStop, "Execute")
@patch.object(main.CommandRun, "Execute")
@patch.object(main.CommandMoveTo, "Execute")
class TestExceptionHandlers(unittest.TestCase):
    def setUp(self) -> None:
        self.game = main.GameCommand()
        self.stateNormal = main.StateNormal(self.game.gameQueue)
        self.stateMoveTo = main.StateMoveTo(self.game.gameQueue, self.stateNormal)

    def test_StopCommandFromNormalState(self, moveTo, run, hardStop, regular):
        with patch.object(main.StateNormal, "Handle", wraps=self.stateNormal.Handle) as stateNormalHandle:
            with patch.object(main.StateMoveTo, "Handle", wraps=self.stateMoveTo.Handle) as stateMoveToHandle:
                self.game.gameQueue.append(main.CommandRegular())
                self.game.gameQueue.append(main.CommandHardStop())
                self.game.Execute()
                assert regular.call_count == 1
                assert hardStop.call_count == 1
                assert moveTo.call_count == 0
                assert run.call_count == 0
                assert stateNormalHandle.call_count == 2
                assert stateMoveToHandle.call_count == 0

    def test_SwitchToMoveToStateAndStop(self, moveTo, run, hardStop, regular):
        with patch.object(main.StateNormal, "Handle", wraps=self.stateNormal.Handle) as stateNormalHandle:
            with patch.object(main.StateMoveTo, "Handle", wraps=self.stateMoveTo.Handle) as stateMoveToHandle:
                self.game.gameQueue.append(main.CommandMoveTo())
                self.game.gameQueue.append(main.CommandRegular())
                self.game.gameQueue.append(main.CommandHardStop())
                self.game.Execute()
                assert regular.call_count == 1
                assert hardStop.call_count == 1
                assert moveTo.call_count == 1
                assert run.call_count == 0
                assert stateNormalHandle.call_count == 1
                assert stateMoveToHandle.call_count == 2

    def test_SwitchToNormalStateAndStop(self, moveTo, run, hardStop, regular):
        with patch.object(main.StateNormal, "Handle", wraps=self.stateNormal.Handle) as stateNormalHandle:
            with patch.object(main.StateMoveTo, "Handle", wraps=self.stateMoveTo.Handle) as stateMoveToHandle:
                self.game.gameQueue.append(main.CommandMoveTo())
                self.game.gameQueue.append(main.CommandRegular())
                self.game.gameQueue.append(main.CommandRun())
                self.game.gameQueue.append(main.CommandRegular())
                self.game.gameQueue.append(main.CommandHardStop())
                self.game.Execute()
                assert regular.call_count == 2
                assert hardStop.call_count == 1
                assert moveTo.call_count == 1
                assert run.call_count == 1
                assert stateNormalHandle.call_count == 3
                assert stateMoveToHandle.call_count == 2

    
