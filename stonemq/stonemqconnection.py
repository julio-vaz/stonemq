import pika
import stonemq.exceptions
import contracts

class StoneMQConnection:

    @contracts.contract(appkey='string', hostname='string', port='int', username='string', password='string', prefetch='int,>=1,<10000', heartbeat='int,>=120,<=580')
    def __init__(self, appkey, hostname, port, username, password, prefetch = 1, heartbeat = 580):
        self.appkey = appkey
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.prefetch = prefetch
        self.heartbeat = heartbeat

        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(host=self.hostname, port=self.port,
                                               credentials=credentials)

        try:
            self._connection = pika.BlockingConnection(parameters)
        except pika.exceptions.ConnectionClosed as e:
            raise stonemq.exceptions.ConnectionError
        except pika.exceptions.ProbableAuthenticationError as e:
            raise stonemq.exceptions.InvalidCredentialsError
