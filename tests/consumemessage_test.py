import unittest
from stonemq.stonemqconnection import StoneMQConnection


class ConsumeMessageTests(unittest.TestCase):

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
        self.string_message = "I'm a message, feed me paper."

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
        self.last_received_message = None

    def basic_callback(self, body):
        self.valid_connection.stop_consuming()
        self.last_received_message = body
        self.valid_connection._close_connection()

    def test_ok_consume_dict(self):
        self.valid_connection.send(route=self.route, uri=self.uri,
                                   event=self.event, message=self.dict_message)
        self.valid_connection.consume(route=self.route,
                                      callback=self.basic_callback)
        self.assertEqual(self.last_received_message, self.dict_message)

    def test_ok_consume_string(self):
        self.valid_connection.send(route=self.route,
                                   uri=self.uri,
                                   event=self.event,
                                   message=self.string_message)
        self.valid_connection.consume(route=self.route,
                                      callback=self.basic_callback)
        self.assertEqual(self.last_received_message, self.string_message)
