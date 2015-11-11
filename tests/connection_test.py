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
            connection._close_connection()
        except Exception as e:
          self.fail()

    def test_fail_connection_invalid_hostname(self):
        #null hostname
        def __null_hostname():
            StoneMQConnection(appkey=self.appkey,
                              hostname=None,
                              port=self.port,
                              username=self.user,
                              password=self.password)
        self.assertRaises(contracts.ContractException, __null_hostname)

        #invalid hostname
        def __invalid_hostname():
            StoneMQConnection(appkey=self.appkey,
                              hostname="None",
                              port=self.port,
                              username=self.user,
                              password=self.password)
        self.assertRaises(stonemq.exceptions.ConnectionError, __invalid_hostname)

    def test_fail_connection_invalid_port(self):
        #null port
        def __null_port():
            StoneMQConnection(appkey=self.appkey,
                              hostname=self.hostname,
                              port=None,
                              username=self.user,
                              password=self.password)
        self.assertRaises(contracts.ContractException, __null_port)

        #invalid port
        def __invalid_port():
            StoneMQConnection(appkey=self.appkey,
                              hostname=self.hostname,
                              port=-1,
                              username=self.user,
                              password=self.password)
        self.assertRaises(stonemq.exceptions.ConnectionError, __invalid_port)    

    def test_fail_connection_invalid_credentials(self):
        #null username
        def __null_username():
            StoneMQConnection(appkey=self.appkey,
                              hostname=self.hostname,
                              port=self.port,
                              username=None,
                              password=self.password)
        self.assertRaises(contracts.ContractException, __null_username)

        #invalid username
        def __invalid_username():
            StoneMQConnection(appkey=self.appkey,
                              hostname=self.hostname,
                              port=self.port,
                              username='banana',
                              password=self.password)
        self.assertRaises(stonemq.exceptions.InvalidCredentialsError, 
                          __invalid_username) 

        #null password
        def __null_password():
            StoneMQConnection(appkey=self.appkey,
                              hostname=self.hostname,
                              port=self.port,
                              username=self.user,
                              password=None)
        self.assertRaises(contracts.ContractException, __null_password)

        #invalid password
        def __invalid_password():
            StoneMQConnection(appkey=self.appkey,
                              hostname=self.hostname,
                              port=self.port,
                              username=self.user,
                              password='banana')
        self.assertRaises(stonemq.exceptions.InvalidCredentialsError, 
                          __invalid_password) 

    def test_fail_connection_appkey(self):
        #null Appkey
        def __null_appkey():
            StoneMQConnection(appkey=None,
                              hostname=self.hostname,
                              port=self.port,
                              username=self.user,
                              password=self.password)
        self.assertRaises(contracts.ContractException, __null_appkey)

    def test_invalid_heartbeat_value(self):
        #invalid heartbeat
        def __invalid_heartbeat():
            StoneMQConnection(appkey=self.appkey,
                              hostname=self.hostname,
                              port=self.port,
                              username=self.user,
                              password=self.password,
                              prefetch=self.prefetch,
                              heartbeat=5)
        self.assertRaises(contracts.ContractException, __invalid_heartbeat)

    def test_invalid_prefetch_value(self):
        #invalid prefetch
        def __invalid_heartbeat():
            StoneMQConnection(appkey=self.appkey,
                              hostname=self.hostname,
                              port=self.port,
                              username=self.user,
                              password=self.password,
                              prefetch=-1,
                              heartbeat=self.heartbeat)
        self.assertRaises(contracts.ContractException, __invalid_heartbeat)