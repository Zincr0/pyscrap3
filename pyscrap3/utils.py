from kombu import Connection
from urllib.parse import quote_plus
#from IPython import embed


class rabbitMsg():
    """Envía mensajes a traves de rabbitmq usando 'kombu'
    https://pypi.python.org/pypi/kombu"""

    def __init__(self, queue, user="guest", passw="guest", host="localhost"):
        self.user = user
        self.passw = quote_plus(passw)
        self.host = host
        self.urlRabbit = "amqp://" + self.user + ":" + self.passw + "@" + host + "/"
        self.queueName = queue
        self.open()

    def open(self):
        self.conn = Connection(self.urlRabbit)
        self.cola = self.conn.SimpleQueue(self.queueName)

    def send(self, message):
        self.cola.put(message)

    def get(self):
        message = self.cola.get(block=True)
        result = message.payload
        message.ack()
        return result

    def getIfExists(self):
        message = self.cola.queue.get()
        if message:
            result = message.payload
            message.ack()
            return result
        else:
            return None

    def close(self):
        self.cola.close()
