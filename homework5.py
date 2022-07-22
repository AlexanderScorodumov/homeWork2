import threading
from abc import ABC, abstractmethod
from typing import TypeVar


class Command(ABC):
    @abstractmethod
    def Execute(self) -> None:
        pass


class CommandTest(Command):
    def __init__(self, value) -> None:
        self.value = value

    def Execute(self) -> None:
        print(self.value)


class ScopesStorage(threading.local):
    def __init__(self) -> None:
        super().__init__()
        self._scopes = {"root": {}}
        self._currentScope = self._scopes["root"]

    def NewScope(self, newScope: str) -> None:
        self._scopes[newScope] = {}

    @property
    def scopes(self):
        return self._scopes

    @property
    def currentScope(self):
        return self._currentScope
    
    @currentScope.setter
    def currentScope(self, newCurrentScope: str):
        self._currentScope = self._scopes[newCurrentScope]
 
T = TypeVar('T')
class IoC:
    scopesStorage = ScopesStorage()

    def __init__(self) -> None:
        pass

    class _CommandScopeNew(Command):
        def __init__(self, newScope: str) -> None:
            super().__init__()
            self.newScope = newScope

        def Execute(self) -> None:
            IoC.scopesStorage.NewScope(self.newScope)
            #IoC.scopes[self.newScope] = {}


    class _CommandScopeCurrent(Command):
        def __init__(self, newScope: str) -> None:
            super().__init__()
            self.newScope = newScope

        def Execute(self) -> None:
            if self.newScope in IoC.scopesStorage.scopes:
                IoC.scopesStorage.currentScope = self.newScope
            else:
                raise AttributeError("Non-existent scope: %s", self.newScope)

    @staticmethod
    def Resolve(type: T, key: str, *args) -> T:
        if key == "IoC.Register":
            try:
                IoC.scopesStorage.currentScope[str(args[0])] = args[1]
                return IoC.scopesStorage.currentScope[args[0]]()
            except:
                raise AttributeError("Unsupperted arguments for 'IoC.Register': %s", args)
        elif key == "Scopes.New":    
            try:
                return IoC._CommandScopeNew(str(args[0]))
            except:
                raise AttributeError("Unsupperted arguments for 'Scopes.New': %s", args)  
        elif key == "Scopes.Current":    
            try:
                return IoC._CommandScopeCurrent(str(args[0]))
            except:
                raise AttributeError("Unsupperted arguments for 'Scopes.New': %s", args)  
        else:
            try:
                return IoC.scopesStorage.currentScope[key]()
            except:
                try:
                    return IoC.scopesStorage.scopes["root"][key]()
                except:
                    raise AttributeError("%s - unsupported argument for 'Resolve' method" % key)


def SomeFunction():
    threadId = threading.get_ident()
    IoC.Resolve(Command, "Scopes.New", threadId).Execute()
    IoC.Resolve(Command, "Scopes.Current", threadId).Execute()
    IoC.Resolve(Command, "IoC.Register", "CommandA", lambda: CommandTest("Command A from %s" % threadId))
    IoC.Resolve(Command, "IoC.Register", "CommandB", lambda: CommandTest("Command B from %s" % threadId))
    IoC.Resolve(Command, "CommandA").Execute()
    IoC.Resolve(Command, "CommandB").Execute()


if __name__ == '__main__':
    """ print(threading.get_ident())

    IoC.Resolve(Command, "IoC.Register", "CommandA", lambda: CommandTest("Command A from %s" % "Root"))
    IoC.Resolve(Command, "IoC.Register", "CommandB", lambda: CommandTest("Command B from %s" % "Root"))
    IoC.Resolve(Command, "CommandA").Execute()
    IoC.Resolve(Command, "CommandB").Execute() """

    SomeFunction()

    Session1 = threading.Thread(target=SomeFunction)
    Session2 = threading.Thread(target=SomeFunction)   

    Session1.start()
    IoC.Resolve(Command, "CommandA").Execute()
    IoC.Resolve(Command, "CommandB").Execute()
    Session2.start()
    IoC.Resolve(Command, "CommandA").Execute()
    IoC.Resolve(Command, "CommandB").Execute()

    Session1.join()
    Session2.join()

    threadId = threading.get_ident()
    print(threadId)
    #IoC.Resolve(Command, "Scopes.Current", threadId).Execute()
    IoC.Resolve(Command, "CommandA").Execute()
    IoC.Resolve(Command, "CommandB").Execute()