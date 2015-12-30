"""
Unity Connection server will be required for these tests
Tests are performed against CUC 10.5.2
"""
import unittest
import requests

from requests.exceptions import ConnectTimeout
from cupi.cake import CUPI

requests.packages.urllib3.disable_warnings()


class TestCUPI(unittest.TestCase):

    def setUp(self):
        self.cuc = CUPI('192.168.200.11', 'admin', 'asdfpoiu')

    def test_connection_to_cuc_server_timeout_with_incorrect_ip_fail(self):
        c = CUPI('192.168.200.111', 'admin', 'asdfpoiu')
        self.assertRaises(ConnectTimeout, c.online_test)

    def test_connection_to_cuc_server_timeout_with_correct_ip(self):
        self.assertEqual(self.cuc.online_test(), 200)

    def test_get_languages_method_returns_200_ok_and_dict_key_exists(self):
        result = self.cuc.get_languages()
        self.assertEqual(result[0], 200) and 'LanguageMapping' in result[1]

    def test_get_owner_location_oid_returns_200_ok_and_oid_string(self):
        result = self.cuc.get_owner_location_oid()
        self.assertEqual(result[0], 200) and result[1] != ''

    def test_get_schedule_sets_method_full_returns_200_ok_and_dict_key_exists(self):
        result = self.cuc.get_schedule_sets(mini=False)
        self.assertEqual(result[0], 200) and 'ScheduleSet' in result[1]

    def test_get_schedule_sets_method_mini_returns_list(self):
        result = self.cuc.get_schedule_sets(mini=True)
        self.assertTrue(isinstance(result, list))

    def test_get_schedules_method_full_returns_200_ok_and_dict_key_exists(self):
        result = self.cuc.get_schedules(mini=False)
        self.assertEqual(result[0], 200) and 'Schedule' in result[1]

    def test_get_schedules_method_mini_returns_list(self):
        result = self.cuc.get_schedules(mini=True)
        self.assertTrue(isinstance(result, list))

    def test_get_schedule_method_returns_schedule_oid(self):
        schedule_oid = self.cuc.get_schedules(mini=True)[0][1]
        result = self.cuc.get_schedule(schedule_oid)['ObjectId']
        self.assertEqual(result, schedule_oid)

    def test_get_schedule_method_with_unknown_oid_returns_404(self):
        result = self.cuc.get_schedule('1234567890')
        self.assertEqual(result, 'Schedule not found')

