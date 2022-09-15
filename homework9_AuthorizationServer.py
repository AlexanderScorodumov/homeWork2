from __future__ import annotations
import os
import sys
from typing import Dict, List
import jwt
import json
import pika
import logging

class AuthorizationServer:
    def __init__(self) -> None:
        self.messagePayload = {}
        self.games: Dict[int, List[str]] = {}
        self.messageDict = {
            "createGame": lambda: self.CreateGame(),
            "getToken": lambda: self.GetToken()
        }

    
    def HandleException(self, str: str):
        logging.error(str)

          
    def CreateGame(self):
        gameId = len(self.games.keys())+1
        try:
            users = self.messagePayload["users"]
            self.games[gameId] = users
            logging.info("Game #{} created. Users: {}".format(gameId, users))
        except Exception as ex:
            self.HandleException("Create game failed. Info {}".format(ex))

    def GetToken(self):
        try:
            gameId = self.messagePayload["gameId"]
            users = self.games[gameId]
            user = self.messagePayload["user"]
            if user in users:
                tokenDict = {"gameId": gameId, "user": user, "validity": True}
            else:
                tokenDict = {"gameId": gameId, "user": user, "validity": False}
            logging.info("Token for user {} in game #{} created. Token: {}".format(user, gameId, tokenDict))
            self.SendToken(dict=tokenDict)
        except Exception as ex:
            self.HandleException("Get token failed. Info {}".format(ex))


    def SendToken(self, dict):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='GameServer')
        encodedJwt = jwt.encode(dict, "secret", algorithm="HS256")
        payload = '{"token": "%s"}' % encodedJwt
        channel.basic_publish(exchange='', routing_key='GameServer', body=payload)
        print(" [x] Sent %s" % payload)
        connection.close()

    
    def ParseMessage(self):
        try:
            messageId = self.messagePayload["message"]
            self.messageDict[messageId]()
        except Exception as ex:
            self.HandleException("Incoorrect message format. Info {}".format(ex))

    def GetMessage(self):
        queueName = 'AuthorizationServer'
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=queueName)

        def callback(ch, method, properties, data):
            logging.info(" [x] Received {}".format(data))
            try:
                self.messagePayload = json.loads(data)
                self.ParseMessage()
            except Exception as ex:
                logging.info("Incoorrect JSON format. Info {}".format(ex))

        channel.basic_consume(queue=queueName, on_message_callback=callback, auto_ack=True)
        logging.info(' [*] Waiting for messages at {}. To exit press CTRL+C'.format(queueName))
        channel.start_consuming()


if __name__ == '__main__':
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    server = AuthorizationServer()
    try:
        server.GetMessage()
    except KeyboardInterrupt:
        logging.info('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)