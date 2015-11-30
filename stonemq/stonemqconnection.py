#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pika
import stonemq.exceptions
import contracts
import json
import time
from bson import json_util


class StoneMQConnection:
    @contracts.contract(appkey='string', hostname='string', port='int',
                        username='string', password='string',
                        prefetch='int,>=1,<10000', heartbeat='int,>=120,<=580')
    def __init__(self, appkey, hostname, port, username, password, prefetch=1,
                 heartbeat=580):
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

    @contracts.contract(route='string', event='string', uri='string')
    def send(self, route, event, message, uri='', reconnection_trial=0):

        if reconnection_trial == 3:
            raise stonemq.exceptions.ConnectionRefused

        body = self._resolve_message(route, event, message, uri)
        try:
            self._channel.basic_publish(exchange=route, routing_key='',
                                        body=body)

        # More information http://www.rabbitmq.com/amqp-0-9-1-reference.html
        except pika.exceptions.ChannelClosed as e1:
            if(e1.args[0] == 403):
                raise stonemq.exceptions.InsufficientPermissionsError
            elif(e1.args[0] == 404):
                raise stonemq.exceptions.RouteNotFoundError
        except pika.exceptions.ConnectionClosed as e2:
            if(e2.args[0] == 320):
                time.sleep(1)
                self.send(self, route, event, message, uri,
                          reconnection_trial + 1)

    # TODO: Incluir no 'contrato' de consumo os mesmos parametros passados
    # quando a mensagem é produzida (route, evento, uri, appkey)
    @contracts.contract(route='string')
    def consume(self, route, callback):
        self.should_consume = True
        self.outer_callback = callback
        self._channel.basic_consume(self._callback, queue=route,
                                    no_ack=True)
        while self.should_consume:
            self._connection.process_data_events()

    def stop_consuming(self, close_connection=False):
        self.should_consume = False
        if close_connection:
            self._close_connection()

    def _callback(self, channel, method, properties, body):
        try:
            mod_body = json.loads(body, object_hook=json_util.object_hook)
        # TODO: Incluir teste para isso
        # TODO: Jogar pra fila de erro quando dá merda
        except ValueError:
            raise stonemq.exceptions.ConsumedMessageIsNotJsonError
        self.outer_callback(mod_body)

    def _close_connection(self):
        self._channel.close()
        self._connection.close()

    def _connect(self, parameters):
        try:
            self._connection = pika.BlockingConnection(parameters)
        except pika.exceptions.ConnectionClosed:
            raise stonemq.exceptions.ConnectionError
        except pika.exceptions.ProbableAuthenticationError:
            raise stonemq.exceptions.InvalidCredentialsError

        self._channel = self._connection.channel()
        self._channel.basic_qos(prefetch_count=self.prefetch)
        self._channel.confirm_delivery()

    def _resolve_message(self, route, event, message, uri):
        resolved_message = {
            'appkey': self.appkey,
            'event': event,
            'uri': uri,
            'content': message
        }
        return json.dumps(resolved_message, default=json_util.default)
