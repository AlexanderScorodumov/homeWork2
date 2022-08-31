import threading
from abc import ABC, abstractmethod
from typing import Callable, Dict, TypeVar


class Command(ABC):
    @abstractmethod
    def Execute(self) -> None:
        pass


class CommandTest(Command):
    def __init__(self, value) -> None:
        self.value = value

    def Execute(self) -> None:
        print(self.value)


class Scope(threading.local):
    def __init__(self, scopesStorage: Dict[str, Dict[str, Callable]]) -> None:
        super().__init__()
        self._scopesStorage = scopesStorage
        self._scope: Dict[str, Callable] = self._scopesStorage[list(self._scopesStorage.keys())[0]]

    @property
    def scope(self):
        return self._scope
    
    @scope.setter
    def scope(self, scopeName: str):
        self._scope = self._scopesStorage[scopeName]
 
T = TypeVar('T')
class IoC:
    scopesStorage: Dict[str, Dict[str, Callable]] = {"root": {}}
    scopeLocal: Dict[str, Callable] = Scope(scopesStorage=scopesStorage)


    def __init__(self) -> None:
        pass


    class _CommandRegister(Command):
        def __init__(self, name: str, function: Callable) -> None:
            super().__init__()
            self.name = name
            self.function = function

        def Execute(self) -> None:
            IoC.scopeLocal.scope[self.name] = self.function


    class _CommandScopeNew(Command):
        def __init__(self, newScope: str) -> None:
            super().__init__()
            self.newScope = newScope

        def Execute(self) -> None:
            IoC.scopesStorage[self.newScope] = {}


    class _CommandScopeCurrent(Command):
        def __init__(self, newScope: str) -> None:
            super().__init__()
            self.newScope = newScope

        def Execute(self) -> None:
            if self.newScope in IoC.scopesStorage.keys():
                IoC.scopeLocal.scope = self.newScope
            else:
                raise AttributeError("Non-existent scope: %s", self.newScope)

    @staticmethod
    def Resolve(type: T, key: str, *args) -> T:
        if key == "IoC.Register":
            try:
                return IoC._CommandRegister(str(args[0]), args[1])
            except:
                raise AttributeError("Unsupported arguments for 'IoC.Register': %s", args)
        elif key == "Scopes.New":    
            try:
                return IoC._CommandScopeNew(str(args[0]))
            except:
                raise AttributeError("Unsupported arguments for 'Scopes.New': %s", args)  
        elif key == "Scopes.Current":    
            try:
                return IoC._CommandScopeCurrent(str(args[0]))
            except:
                raise AttributeError("Unsupported arguments for 'Scopes.New': %s", args)  
        else:
            try:
                return IoC.scopeLocal.scope[str(key)](*args)
            except:
                try:
                    return IoC.scopesStorage["root"][key](*args)
                except:
                    raise AttributeError("%s - unsupported argument for 'Resolve' method" % key)