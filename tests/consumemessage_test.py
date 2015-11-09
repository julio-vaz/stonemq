import unittest
import stonemq.exceptions
import contracts
from stonemq.stonemqconnection import StoneMQConnection
import time
import threading

class ConsumeMessageTests(unittest.TestCase):

    def setup_method(self, method):

        self.route = "test"
        self.invalid_route = 'cia'
        self.event = "Test"
        self.uri = "www.hostname.com"
        self.message = {"ID": 0, "Name": "BananaMae", "Bananas": [{"Type": "DaTerra"}, {"Type": "DaAgua"}]}

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
        self.message = None

    def callback(self, message):
        self.message = message

    def test_ok_consumer(self):
        self.connection.send(route=self.route, uri=self.uri, event=self.event, message=self.message)
        while self.message == None:
            time.spleep(0.05)
