"""
Unity Connection server will be required for these tests
Tests are performed against CUC 10.5.2
"""
import unittest

from requests.exceptions import ConnectTimeout

from cupi.cake import CUPI


class TestCUPI(unittest.TestCase):

    def setUp(self):
        self.cuc = CUPI('192.168.200.11', 'admin', 'asdfpoiu')

    def test_connection_to_cuc_server_timeout_with_incorrect_ip_fail(self):
        c = CUPI('192.168.200.111', 'admin', 'asdfpoiu')
        self.assertRaises(ConnectTimeout, c.get_owner_location_oid())

    def test_connection_to_cuc_server_timeout_with_correct_ip_pass(self):
        self.assertEqual(self.cuc.online_test(), 200)



