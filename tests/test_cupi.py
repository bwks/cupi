"""
Unity Connection server will be required for these tests
Tests are performed against CUC 10.5.2
"""
import unittest

from requests.exceptions import ConnectTimeout
from cupi.cake import CUPI


class TestCUPI(unittest.TestCase):

    def setUp(self):
        self.cuc = CUPI('192.168.200.11', 'admin', 'asdfpoiu', disable_warnings=True)

    def test_connection_to_cuc_server_timeout_with_incorrect_ip(self):
        c = CUPI('192.168.200.111', 'admin', 'asdfpoiu')
        self.assertRaises(ConnectTimeout, c.online_test)

    def test_connection_to_cuc_server_with_correct_ip(self):
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

    def test_get_users_method_full_returns_200_ok_and_dict_key_exists(self):
        result = self.cuc.get_users(mini=False)
        self.assertEqual(result[0], 200) and 'User' in result[1]

    def test_get_users_method_mini_returns_list(self):
        result = self.cuc.get_users(mini=True)
        self.assertTrue(isinstance(result, list))

    def test_get_user_call_handler_oid_returns_non_empty_string(self):
        user_oid = self.cuc.get_users(mini=True)[0][2]
        result = self.cuc.get_user_call_handler_oid(user_oid)
        self.assertIsNot(result, '')

    def test_get_user_method_returns_schedule_oid(self):
        user_oid = self.cuc.get_users(mini=True)[0][2]
        result = self.cuc.get_user(user_oid)['ObjectId']
        self.assertEqual(result, user_oid)

    def test_get_user_method_with_unknown_oid_returns_404(self):
        result = self.cuc.get_user('1234567890')
        self.assertEqual(result, 'User not found')

    def test_get_user_pin_settings_method_returns_user_oid(self):
        user_oid = self.cuc.get_users(mini=True)[0][2]
        result = self.cuc.get_user_pin_settings(user_oid)['UserObjectId']
        self.assertEqual(result, user_oid)

    def test_get_user_pin_settings_method_with_unknown_oid_returns_404(self):
        result = self.cuc.get_user_pin_settings('1234567890')
        self.assertEqual(result, 'User not found')

    def test_get_user_password_settings_method_returns_user_oid(self):
        user_oid = self.cuc.get_users(mini=True)[0][2]
        result = self.cuc.get_user_password_settings(user_oid)['UserObjectId']
        self.assertEqual(result, user_oid)

    def test_get_user_password_settings_method_with_unknown_oid_returns_404(self):
        result = self.cuc.get_user_password_settings('1234567890')
        self.assertEqual(result, 'User not found')

    def test_get_user_templates_method_returns_list(self):
        result = self.cuc.get_user_templates()
        self.assertTrue(isinstance(result, list))

    def test_get_call_handler_template_oid_returns_non_empty_string(self):
        result = self.cuc.get_call_handler_template_oid()
        self.assertIsNot(result, '')

    def test_get_call_handlers_method_full_returns_200_ok_and_dict_key_exists(self):
        result = self.cuc.get_call_handlers(mini=False)
        self.assertEqual(result[0], 200) and 'Schedule' in result[1]

    def test_get_call_handlers_method_mini_returns_list(self):
        result = self.cuc.get_call_handlers(mini=True)
        self.assertTrue(isinstance(result, list))

    def test_get_call_handler_method_returns_call_handler_oid(self):
        call_handler_oid = self.cuc.get_call_handlers(mini=True)[0][1]
        result = self.cuc.get_call_handler(call_handler_oid)['ObjectId']
        self.assertEqual(result, call_handler_oid)

    def test_get_call_handler_method_with_unknown_oid_returns_404(self):
        result = self.cuc.get_call_handler('1234567890')
        self.assertEqual(result, 'Call handler not found')

    def test_get_call_handler_greeting_method_returns_invalid_greeting_for_unknown_greeting_type(self):
        call_handler_oid = self.cuc.get_call_handlers(mini=True)[0][1]
        greeting = 'blah'
        result = self.cuc.get_call_handler_greeting(call_handler_oid, greeting=greeting)
        self.assertEqual(result, 'Invalid greeting: {0}'.format(greeting))

    def test_get_call_handler_greetings_method_returns_list(self):
        call_handler_oid = self.cuc.get_call_handlers(mini=True)[0][1]
        result = self.cuc.get_call_handler_greetings(call_handler_oid)['Greeting']
        self.assertTrue(isinstance(result, list))

    def test_get_call_handler_greetings_method_with_unknown_oid_returns_404(self):
        result = self.cuc.get_call_handler('1234567890')
        self.assertEqual(result, 'Call handler not found')

    def test_get_call_handler_greeting_method_with_unknown_oid_returns_404(self):
        result = self.cuc.get_call_handler_greeting('1234567890')
        self.assertEqual(result, 'Call handler not found')

    def test_get_call_handler_greeting_method_returns_call_handler_oid(self):
        call_handler_oid = self.cuc.get_call_handlers(mini=True)[0][1]
        result = self.cuc.get_call_handler_greeting(call_handler_oid, greeting='Standard')['CallHandlerObjectId']
        self.assertEqual(result, call_handler_oid)

    def test_get_call_handler_greeting_method_with_off_hours_returns_off_hours_greeting(self):
        call_handler_oid = self.cuc.get_call_handlers(mini=True)[0][1]
        result = self.cuc.get_call_handler_greeting(call_handler_oid, greeting='Off Hours')['GreetingType']
        self.assertEqual(result, 'Off Hours')

    def test_get_caller_input_method_returns_list(self):
        call_handler_oid = self.cuc.get_call_handlers(mini=True)[0][1]
        result = self.cuc.get_caller_input(call_handler_oid)
        self.assertTrue(isinstance(result, list))

    def test_get_caller_input_method_with_unknown_oid_returns_404(self):
        result = self.cuc.get_caller_input('1234567890')
        self.assertEqual(result, 'Call handler not found')
