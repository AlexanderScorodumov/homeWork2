import os
import sys
import jwt
import json
import pika
import logging


class GameServer:
    def __init__(self) -> None:
        self.messagePayload = {}

    
    def HandleException(self, str: str):
        logging.error(str)


    def ParseMessage(self):
        try:
            token = self.messagePayload["token"]
        except Exception as ex:
            self.HandleException("Incoorrect message format. Info {}".format(ex))
        try:
            decode_jwt = jwt.decode(token , "secret", algorithms=["HS256"])
            logging.info(decode_jwt)
        except Exception as ex:
            self.HandleException("Invalid JWT {}".format(ex))
        

    def GetMessage(self):
        queueName = 'GameServer'
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=queueName)

        def callback(ch, method, properties, data):
            logging.info(" [x] Received {}".format(data))
            try:
                self.messagePayload = json.loads(data)
                self.ParseMessage()
            except Exception as ex:
                self.HandleException("Incoorrect JSON format. Info {}".format(ex))

        channel.basic_consume(queue=queueName, on_message_callback=callback, auto_ack=True)
        logging.info(' [*] Waiting for messages at {}. To exit press CTRL+C'.format(queueName))
        channel.start_consuming()


if __name__ == '__main__':
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    server = GameServer()
    try:
        server.GetMessage()
    except KeyboardInterrupt:
        logging.info('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)