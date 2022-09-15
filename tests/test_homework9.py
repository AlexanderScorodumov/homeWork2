import unittest
from unittest.mock import Mock, patch
import concurrent.futures
import homework9_AuthorizationServer as autorizationServer
import homework9_GameServer as gameServer


class TestExceptionHandlers(unittest.TestCase):
    def setUp(self) -> None:
        self.gameServer = gameServer.GameServer()
        self.autorizationServer = autorizationServer.AuthorizationServer()

    def test_GameServer_JwtCorrect(self):       
        with patch.object(gameServer.GameServer, 'HandleException') as handleException:
            self.gameServer.messagePayload = {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJnYW1lSWQiOjEsInVzZXIiOiJBbGV4IiwidmFsaWRpdHkiOiJUcnVlIn0.b27CWPdkWBy6E99_oDzzkFH3XvIIDg6NPJJBGlraU8o"}
            self.gameServer.ParseMessage()
            assert handleException.call_count == 0


    def test_GameServer_JwtNotCorrect(self):       
        with patch.object(gameServer.GameServer, 'HandleException') as handleException:
            self.gameServer.messagePayload = {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJnYW1lSWQiOjEsInVzZXIiOiJBbGV4IiwidmFsaWRpdHkiOiJUcnVlIn0.cgSk-4Lcoo1dEwx8HBuCMK-hX62AoxHclOtb8m5hKv8"}
            self.gameServer.ParseMessage()
            assert handleException.call_count == 1

    
    def test_GameServer_JsonNorCorrect(self):       
        with patch.object(gameServer.GameServer, 'HandleException') as handleException:
            self.gameServer.messagePayload = {"toke": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJnYW1lSWQiOjEsInVzZXIiOiJBbGV4IiwidmFsaWRpdHkiOiJUcnVlIn0.b27CWPdkWBy6E99_oDzzkFH3XvIIDg6NPJJBGlraU8o"}
            self.gameServer.ParseMessage()
            assert handleException.call_count == 2

        
    def test_AuthorizationServer_JsonNotCorrect(self):       
        with patch.object(autorizationServer.AuthorizationServer, 'HandleException') as handleException:
            with patch.object(autorizationServer.AuthorizationServer, 'CreateGame', wraps=self.autorizationServer.CreateGame) as createGame:
                with patch.object(autorizationServer.AuthorizationServer, 'GetToken', wraps=self.autorizationServer.GetToken) as getToken:
                    self.autorizationServer.messagePayload = {"message": "test"}
                    self.autorizationServer.ParseMessage()
                    assert handleException.call_count == 1
                    assert createGame.call_count == 0
                    assert getToken.call_count == 0


    def test_AuthorizationServer_GameCreate(self):       
        with patch.object(autorizationServer.AuthorizationServer, 'HandleException') as handleException:
            with patch.object(autorizationServer.AuthorizationServer, 'CreateGame', wraps=self.autorizationServer.CreateGame) as createGame:
                    self.autorizationServer.messagePayload = {"message": "createGame", "users": ["user1", "uesr2"]}
                    self.autorizationServer.ParseMessage()
                    assert handleException.call_count == 0
                    assert createGame.call_count == 1


    def test_AuthorizationServer_GetTokenFromValidUser(self):       
        with patch.object(autorizationServer.AuthorizationServer, 'HandleException') as handleException:
            with patch.object(autorizationServer.AuthorizationServer, 'CreateGame', wraps=self.autorizationServer.CreateGame) as createGame:
                with patch.object(autorizationServer.AuthorizationServer, 'GetToken', wraps=self.autorizationServer.GetToken) as getToken:
                    with patch.object(autorizationServer.AuthorizationServer, 'SendToken') as sendToken:
                        self.autorizationServer.messagePayload = {"message": "createGame", "users": ["user1", "uesr2"]}
                        self.autorizationServer.ParseMessage()
                        assert handleException.call_count == 0
                        assert createGame.call_count == 1
                        assert getToken.call_count == 0
                        self.autorizationServer.messagePayload = {"message": "getToken", "gameId": 1, "user": "user1"}
                        self.autorizationServer.ParseMessage()
                        assert handleException.call_count == 0
                        assert createGame.call_count == 1
                        assert getToken.call_count == 1
                        assert sendToken.call_count == 1
                        assert sendToken.call_args.kwargs['dict']['validity'] == True


    def test_AuthorizationServer_GetTokenFromInvalidUser(self):       
        with patch.object(autorizationServer.AuthorizationServer, 'HandleException') as handleException:
            with patch.object(autorizationServer.AuthorizationServer, 'CreateGame', wraps=self.autorizationServer.CreateGame) as createGame:
                with patch.object(autorizationServer.AuthorizationServer, 'GetToken', wraps=self.autorizationServer.GetToken) as getToken:
                    with patch.object(autorizationServer.AuthorizationServer, 'SendToken') as sendToken:
                        self.autorizationServer.messagePayload = {"message": "createGame", "users": ["user1", "uesr2"]}
                        self.autorizationServer.ParseMessage()
                        assert handleException.call_count == 0
                        assert createGame.call_count == 1
                        assert getToken.call_count == 0
                        self.autorizationServer.messagePayload = {"message": "getToken", "gameId": 1, "user": "user3"}
                        self.autorizationServer.ParseMessage()
                        assert handleException.call_count == 0
                        assert createGame.call_count == 1
                        assert getToken.call_count == 1
                        assert sendToken.call_count == 1
                        assert sendToken.call_args.kwargs['dict']['validity'] == False