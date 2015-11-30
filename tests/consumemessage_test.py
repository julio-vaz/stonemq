#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from stonemq.stonemqconnection import StoneMQConnection


class ConsumeMessageTests(unittest.TestCase):

    def setup_method(self, method):

        # Message content
        self.open_route = "open.test"
        self.closed_route = 'closed.test'
        self.event = "Test"
        self.uri = "www.hostname.com"
        self.dict_message = {'ID': 0, 'Name': 'BananaMae',
                             'Bananas': [
                                          {'Type': 'DaTerra'},
                                          {'Type': 'DaAgua'}
                                        ]
                             }
        self.string_message = "I'm a message, feed me paper."

        # Connection
        hostname = '172.16.134.99'
        port = 5672
        admin_user = 'admin'
        admin_password = '12345'
        management_user = 'testuser'
        management_password = '123456'
        appkey = ''
        self.admin_connection = StoneMQConnection(appkey=appkey,
                                                  hostname=hostname,
                                                  port=port,
                                                  username=admin_user,
                                                  password=admin_password)

        self.management_connection = StoneMQConnection(
          appkey=appkey,
          hostname=hostname,
          port=port,
          username=management_user,
          password=management_password)

        # Resolving messages
        self.resolved_dict_message = {
                                          'appkey': appkey,
                                          'event': self.event,
                                          'uri': self.uri,
                                          'content': self.dict_message
                                      }
        self.resolved_string_message = {
                                          'appkey': appkey,
                                          'event': self.event,
                                          'uri': self.uri,
                                          'content': self.string_message
                                      }

        self.last_received_message = None

    def basic_callback(self, body):
        self.last_received_message = body
        self.admin_connection.stop_consuming(close_connection=True)

    def test_ok_consume_dict(self):
        self.admin_connection.send(route=self.closed_route, uri=self.uri,
                                   event=self.event, message=self.dict_message)
        self.admin_connection.consume(route=self.closed_route,
                                      callback=self.basic_callback)
        self.assertEqual(self.last_received_message,
                         self.resolved_dict_message)

    def test_ok_consume_string(self):
        self.admin_connection.send(route=self.closed_route,
                                   uri=self.uri,
                                   event=self.event,
                                   message=self.string_message)
        self.admin_connection.consume(route=self.closed_route,
                                      callback=self.basic_callback)
        self.assertEqual(self.last_received_message,
                         self.resolved_string_message)

    def test_fail_consume_invalid_route(self):
        pass
