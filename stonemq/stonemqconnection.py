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

        self._channel = self._connection.channel()
        self._channel.add_on_return_callback(self.callback)
        self.successful = True

    def callback(self, channel, method, properties, body):
        self.successful = False

    @contracts.contract(route='string', event='string', uri='string')
    def send(self, route, event, message, uri=''):
        body = _resolve_message(route, event, message, uri)
        self._channel.basic_publish(exchange=route, routing_key='', body=body)

    def _resolve_message(self, route, event, message, uri):
        return message
