from importlib.util import set_loader
import unittest
import threading
from unittest.mock import Mock, patch
import homework5 as main


class TestExceptionHandlers(unittest.TestCase):
    class TestCommand(main.Command):
        def __init__(self) -> None:
            super().__init__()


        def Execute(self) -> None:
            return super().Execute()


    def setUp(self):
        main.IoC.scopesStorage = main.ScopesStorage()
    

    def tearDown(self):
        main.IoC.scopesStorage.scopes.clear()
        main.IoC.scopesStorage.currentScope.clear()
        pass


    def threadingFunction(self):
        threadId = threading.get_ident()
        main.IoC.Resolve(main.Command, "Scopes.New", threadId).Execute()
        main.IoC.Resolve(main.Command, "Scopes.Current", threadId).Execute()
        main.IoC.Resolve(main.Command, "IoC.Register", "CommandTest", lambda: self.TestCommand())
        main.IoC.Resolve(main.Command, "CommandTest").Execute()
    

    def test_IoCRegisterExecption(self):
        with self.assertRaises(Exception):
            main.IoC.Resolve(main.Command, "IoC.Register")


    def test_IoCScoreNewExecption(self):
        with self.assertRaises(Exception):
            main.IoC.Resolve(main.Command, "Scopes.New")


    def test_IoCScoreCurrentExecption(self):
        with self.assertRaises(Exception):
            main.IoC.Resolve(main.Command, "Scopes.Current")


    def test_IoCScoreCurrentNonExistentExecption(self):
        with self.assertRaises(Exception):
            main.IoC.Resolve(main.Command, "Scopes.Current", "test").Execute()


    def test_IoCUnregisteredDependencyExecption(self):
        with self.assertRaises(Exception):
            main.IoC.Resolve(main.Command, "Test")


    @patch.object(TestCommand, 'Execute')
    def test_IoCCommandExecute(self, testCommand):
        main.IoC.Resolve(main.Command, "IoC.Register", "CommandTest", lambda: self.TestCommand())
        main.IoC.Resolve(main.Command, "CommandTest").Execute()
        assert testCommand.call_count == 1


    def test_IoCScopeNew(self):
        assert len(main.IoC.scopesStorage.scopes) == 1
        assert main.IoC.scopesStorage.currentScope == main.IoC.scopesStorage.scopes["root"]
        main.IoC.Resolve(main.Command, "Scopes.New", "test").Execute()
        assert len(main.IoC.scopesStorage.scopes) == 2
        assert main.IoC.scopesStorage.currentScope == main.IoC.scopesStorage.scopes["root"]


    def test_IoCScopeCurrent(self):
        assert len(main.IoC.scopesStorage.scopes) == 1
        assert main.IoC.scopesStorage.currentScope == main.IoC.scopesStorage.scopes["root"]
        main.IoC.Resolve(main.Command, "Scopes.New", "test").Execute()
        main.IoC.Resolve(main.Command, "Scopes.Current", "test").Execute()
        assert len(main.IoC.scopesStorage.scopes) == 2
        assert main.IoC.scopesStorage.currentScope == main.IoC.scopesStorage.scopes["test"]

    @patch.object(TestCommand, 'Execute')
    def test_IoCFromDifferentThreads(self, testCommand):
        assert len(main.IoC.scopesStorage.scopes) == 1
        assert main.IoC.scopesStorage.currentScope == main.IoC.scopesStorage.scopes["root"]
        self.threadingFunction()
        assert len(main.IoC.scopesStorage.scopes) == 2
        assert main.IoC.scopesStorage.currentScope == main.IoC.scopesStorage.scopes[str(threading.get_ident())]
        assert testCommand.call_count == 1
        thread1 = threading.Thread(target=self.threadingFunction)
        thread2 = threading.Thread(target=self.threadingFunction)
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        assert len(main.IoC.scopesStorage.scopes) == 2
        assert main.IoC.scopesStorage.currentScope == main.IoC.scopesStorage.scopes[str(threading.get_ident())]
        assert testCommand.call_count == 3
