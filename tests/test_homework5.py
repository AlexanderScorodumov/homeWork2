from importlib.util import set_loader
from typing import Callable, Dict
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
        main.IoC.scopesStorage: Dict[str, Dict[str, Callable]] = {"root": {}}
        main.IoC.scopeLocal = main.Scope(scopesStorage=main.IoC.scopesStorage)
        pass
    

    def tearDown(self):
        main.IoC.scopesStorage.clear()
        pass


    def threadingFunction(self):
        threadId = threading.get_ident()
        main.IoC.Resolve(main.Command, "Scopes.New", threadId).Execute()
        main.IoC.Resolve(main.Command, "Scopes.Current", threadId).Execute()
        main.IoC.Resolve(main.Command, "IoC.Register", "CommandTest", lambda: self.TestCommand()).Execute()
        main.IoC.Resolve(main.Command, "CommandTest").Execute()
    

    def test_IoCRegisterExecption(self):
        with self.assertRaises(Exception):
            main.IoC.Resolve(main.Command, "IoC.Register").Execute()


    def test_IoCScoreNewExecption(self):
        with self.assertRaises(Exception):
            main.IoC.Resolve(main.Command, "Scopes.New").Execute()


    def test_IoCScoreCurrentExecption(self):
        with self.assertRaises(Exception):
            main.IoC.Resolve(main.Command, "Scopes.Current").Execute()


    def test_IoCScoreCurrentNonExistentExecption(self):
        with self.assertRaises(Exception):
            main.IoC.Resolve(main.Command, "Scopes.Current", "test").Execute()


    def test_IoCUnregisteredDependencyExecption(self):
        with self.assertRaises(Exception):
            main.IoC.Resolve(main.Command, "Test").Execute()


    @patch.object(TestCommand, 'Execute')
    def test_IoCCommandExecute(self, testCommand):
        main.IoC.Resolve(main.Command, "IoC.Register", "CommandTest", lambda: self.TestCommand()).Execute()
        main.IoC.Resolve(main.Command, "CommandTest").Execute()
        assert testCommand.call_count == 1


    def test_IoCScopeNew(self):
        scopeStorageLength = len(main.IoC.scopesStorage)
        assert main.IoC.scopeLocal.scope == main.IoC.scopesStorage["root"]
        main.IoC.Resolve(main.Command, "Scopes.New", "test").Execute()
        assert len(main.IoC.scopesStorage) == scopeStorageLength + 1
        assert main.IoC.scopeLocal.scope == main.IoC.scopesStorage["root"]


    def test_IoCScopeCurrent(self):
        scopeStorageLength = len(main.IoC.scopesStorage)
        assert main.IoC.scopeLocal.scope == main.IoC.scopesStorage["root"]
        main.IoC.Resolve(main.Command, "Scopes.New", "test").Execute()
        main.IoC.Resolve(main.Command, "Scopes.Current", "test").Execute()
        assert len(main.IoC.scopesStorage) == scopeStorageLength + 1
        assert main.IoC.scopeLocal.scope == main.IoC.scopesStorage["test"]

    @patch.object(TestCommand, 'Execute')
    def test_IoCFromDifferentThreads(self, testCommand):
        scopeStorageLength = len(main.IoC.scopesStorage)
        assert main.IoC.scopeLocal.scope == main.IoC.scopesStorage["root"]
        self.threadingFunction()
        assert len(main.IoC.scopesStorage) == scopeStorageLength + 1
        assert main.IoC.scopeLocal.scope == main.IoC.scopesStorage[str(threading.get_ident())]
        assert testCommand.call_count == 1
        thread1 = threading.Thread(target=self.threadingFunction)
        thread2 = threading.Thread(target=self.threadingFunction)
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        assert len(main.IoC.scopesStorage) == scopeStorageLength + 3
        assert main.IoC.scopeLocal.scope == main.IoC.scopesStorage[str(threading.get_ident())]
        assert testCommand.call_count == 3