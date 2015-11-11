import pika
import stonemq.exceptions
import contracts
import json
import collections
from bson import json_util

class StoneMQConnection:
    @contracts.contract(appkey='string', hostname='string', port='int',
                        username='string', password='string', 
                        prefetch='int,>=1,<10000', heartbeat='int,>=120,<=580')
    def __init__(self, appkey, hostname, port, username, password, prefetch = 1,
                 heartbeat = 580):
        self.appkey = appkey
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.prefetch = prefetch
        self.heartbeat = heartbeat
        self.should_consume = False
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(host=self.hostname, 
                                               port=self.port,
                                               credentials=credentials)
        self._connect(parameters)

    def _connect(self, parameters):
        try:
            self._connection = pika.BlockingConnection(parameters)
        except pika.exceptions.ConnectionClosed as e:
            raise stonemq.exceptions.ConnectionError
        except pika.exceptions.ProbableAuthenticationError as e:
            raise stonemq.exceptions.InvalidCredentialsError

        self._channel = self._connection.channel()
        self._channel.confirm_delivery()

    @contracts.contract(route='string', event='string', uri='string')
    def send(self, route, event, message, uri=''):
        body = self._resolve_message(route, event, message, uri)
        try:
            self._channel.basic_publish(exchange=route, routing_key='',
                                        body=body)
        except pika.exceptions.ChannelClosed as e:
            if(e.args[0] == 403):
                raise stonemq.exceptions.InsufficientPermissionsError
            elif(e.args[0] == 404):
                raise stonemq.exceptions.RouteNotFoundError

    def _resolve_message(self, route, event, message, uri):
        return json.dumps(message, default=json_util.default)

    def _close_connection(self):
        try:
            self._channel.close()
            self._connection.close()
        except:
            pass