import pika
import unittest
import stonemq.exceptions
import contracts

from stonemq.stonemqconnection import StoneMQConnection

class UnitConnectionTest(unittest.TestCase):

    def setup_method(self, method):
        ## Mandatory
        self.hostname = '172.16.134.99'
        self.port = 5672
        self.user = 'admin'
        self.password = '12345'
        self.appkey = ''

        ## Optional
        self.prefetch = 1
        self.heartbeat = 520

    def test_ok_connection(self):
        try:
            connection = StoneMQConnection(appkey=self.appkey,
                                           hostname=self.hostname,
                                           port=self.port,
                                           username=self.user,
                                           password=self.password)
        except Exception as e:
            assert False

        assert True

    def test_fail_connection_invalid_hostname(self):
        #null hostname
        try:
            connection = StoneMQConnection(appkey=self.appkey,
                                           hostname=None,
                                           port=self.port,
                                           username=self.user,
                                           password=self.password)
            assert False
        except contracts.ContractException as e:
            assert True
        except Exception as e:
            assert False

        #invalid hostname
        try:
            connection = StoneMQConnection(appkey=self.appkey,
                                           hostname="None",
                                           port=self.port,
                                           username=self.user,
                                           password=self.password)
            assert False
        except stonemq.exceptions.ConnectionError as e:
            assert True
        except Exception as e:
            assert False

    def test_fail_connection_invalid_port(self):
        #null port
        try:
            connection = StoneMQConnection(appkey=self.appkey,
                                           hostname=self.hostname,
                                           port=None,
                                           username=self.user,
                                           password=self.password)
            assert False
        except contracts.ContractException as e:
            assert True
        except Exception as e:
            assert False

        #invalid port
        try:
            connection = StoneMQConnection(appkey=self.appkey,
                                           hostname=self.hostname,
                                           port=-1,
                                           username=self.user,
                                           password=self.password)
            assert False
        except stonemq.exceptions.ConnectionError as e:
            assert True
        except Exception as e:
            assert False

    def test_fail_connection_invalid_credentials(self):
        #null username
        try:
            connection = StoneMQConnection(appkey=self.appkey,
                                           hostname=self.hostname,
                                           port=self.port,
                                           username=None,
                                           password=self.password)
            assert False
        except contracts.ContractException as e:
            assert True
        except Exception as e:
            assert False

        #invalid username
        try:
            connection = StoneMQConnection(appkey=self.appkey,
                                           hostname=self.hostname,
                                           port=self.port,
                                           username='banana',
                                           password=self.password)
            assert False
        except stonemq.exceptions.InvalidCredentialsError as e:
            assert True
        except Exception as e:
            assert False

        #null password
        try:
            connection = StoneMQConnection(appkey=self.appkey,
                                           hostname=self.hostname,
                                           port=self.port,
                                           username=self.user,
                                           password=None)
            assert False
        except contracts.ContractException as e:
            assert True
        except Exception as e:
            assert False

        #invalid password
        try:
            connection = StoneMQConnection(appkey=self.appkey,
                                           hostname=self.hostname,
                                           port=self.port,
                                           username=self.user,
                                           password='banana')
            assert False
        except stonemq.exceptions.InvalidCredentialsError as e:
            assert True
        except Exception as e:
            assert False
