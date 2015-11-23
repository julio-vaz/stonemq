import unittest
import stonemq.exceptions
import contracts
from stonemq.stonemqconnection import StoneMQConnection


class SendMessageTests(unittest.TestCase):

    def setup_method(self, method):

        self.route = "test"
        self.invalid_route = 'cia'
        self.event = "Test"
        self.uri = "www.hostname.com"
        self.dict_message = {'ID': 0, 'Name': 'BananaMae',
                             'Bananas': [
                                          {'Type': 'DaTerra'},
                                          {'Type': 'DaAgua'}
                                        ]
                             }

        hostname = '172.16.134.99'
        port = 5672
        valid_user = 'admin'
        invalid_user = 'testuser'
        valid_password = '12345'
        invalid_password = '123456'
        appkey = ''
        self.valid_connection = StoneMQConnection(appkey=appkey,
                                                  hostname=hostname,
                                                  port=port,
                                                  username=valid_user,
                                                  password=valid_password)

        self.invalid_connection = StoneMQConnection(appkey=appkey,
                                                    hostname=hostname,
                                                    port=port,
                                                    username=invalid_user,
                                                    password=invalid_password)

    def test_ok_send_message(self):
        try:
            self.valid_connection.send(
                route=self.route, event=self.event, message=self.dict_message,
                uri=self.uri)
        except Exception:
            self.fail()

    def test_fail_send_message_invalid_route(self):
        # Null route
        self.assertRaises(contracts.ContractException,
                          self.valid_connection.send,
                          route=None,
                          uri=self.uri,
                          event=self.event,
                          message=self.message)

        # Invalid route
        self.assertRaises(stonemq.exceptions.RouteNotFoundError,
                          self.valid_connection.send,
                          route=self.route+"!", uri=self.uri,
                          event=self.event, message=self.dict_message)

    def test_fail_send_message_invalid_permissions(self):
        # Insufficent permissions
        self.assertRaises(stonemq.exceptions.InsufficientPermissionsError,
                          self.invalid_connection.send,
                          route=self.invalid_route, uri=self.uri,
                          event=self.event, message=self.message)
