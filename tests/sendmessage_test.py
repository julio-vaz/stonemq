#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import stonemq.exceptions
import contracts
from stonemq.stonemqconnection import StoneMQConnection


class SendMessageTests(unittest.TestCase):

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

    def test_ok_admin_send_message(self):
        try:
            self.admin_connection.send(route=self.closed_route,
                                       event=self.event,
                                       message=self.dict_message,
                                       uri=self.uri)
        except Exception:
            self.fail()

    def test_ok_management_send_message(self):
        try:
            self.management_connection.send(route=self.open_route,
                                            event=self.event,
                                            message=self.dict_message,
                                            uri=self.uri)
        except Exception:
            self.fail()

    def test_fail_send_message_invalid_route(self):
        # Null route
        self.assertRaises(contracts.ContractException,
                          self.admin_connection.send,
                          route=None,
                          uri=self.uri,
                          event=self.event,
                          message=self.dict_message)

        # Invalid route
        self.assertRaises(stonemq.exceptions.RouteNotFoundError,
                          self.admin_connection.send,
                          route=self.open_route+"!", uri=self.uri,
                          event=self.event, message=self.dict_message)

    def test_fail_send_message_invalid_permissions(self):
        # Insufficent permissions
        self.assertRaises(stonemq.exceptions.InsufficientPermissionsError,
                          self.management_connection.send,
                          route=self.closed_route, uri=self.uri,
                          event=self.event, message=self.dict_message)

    def test_fail_after_losing_connection(self):
        pass
