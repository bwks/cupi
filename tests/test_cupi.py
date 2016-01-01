"""
Unity Connection server will be required for these tests
Tests are performed against CUC 10.5.2
"""
import unittest

from requests.exceptions import ConnectTimeout
from cupi.cake import CUPI


class TestCUPI(unittest.TestCase):

    def setUp(self):
        self.cuc = CUPI('192.168.200.11', 'admin', 'asdfpoiu', timeout=3, disable_warnings=True)

    def test_connection_to_cuc_server_timeout_with_incorrect_ip(self):
        c = CUPI('192.168.200.111', 'admin', 'asdfpoiu')
        self.assertRaises(ConnectTimeout, c.get_server_info, online_test=True)

    def test_connection_to_cuc_server_with_correct_ip(self):
        self.assertEqual(self.cuc.get_server_info(online_test=True), 200)

    def test_get_license_info_full_returns_dict_and_key_exists(self):
        result = self.cuc.get_license_info(mini=False)
        self.assertTrue(isinstance(result, dict)) and 'LicenseStatusCount' in result

    def test_get_license_info_mini_returns_list(self):
        result = self.cuc.get_license_info(mini=True)
        self.assertTrue(isinstance(result, list))

    def test_get_languages_returns_dict_and_key_exists(self):
        result = self.cuc.get_languages()
        self.assertTrue(isinstance(result, dict)) and 'LanguageMapping' in result

    def test_get_owner_location_oid_returns_oid_string(self):
        result = self.cuc.get_owner_location_oid()
        self.assertNotEqual(result, '')

    def test_get_schedule_sets_full_returns_dict_and_key_exists(self):
        result = self.cuc.get_schedule_sets(mini=False)
        self.assertTrue(isinstance(result, dict)) and 'ScheduleSet' in result

    def test_get_schedule_sets_mini_returns_list(self):
        result = self.cuc.get_schedule_sets(mini=True)
        self.assertTrue(isinstance(result, list))

    def test_get_schedules_full_returns_dict_and_key_exists(self):
        result = self.cuc.get_schedules(mini=False)
        self.assertTrue(isinstance(result, dict)) and 'Schedule' in result

    def test_get_schedules_mini_returns_list(self):
        result = self.cuc.get_schedules(mini=True)
        self.assertTrue(isinstance(result, list))

    def test_get_schedule_returns_schedule_oid(self):
        schedule_oid = self.cuc.get_schedules(mini=True)[0][1]
        result = self.cuc.get_schedule(schedule_oid)['ObjectId']
        self.assertEqual(result, schedule_oid)

    def test_get_schedule_with_unknown_oid_returns_404(self):
        result = self.cuc.get_schedule('1234567890')
        self.assertEqual(result, 'Schedule not found')

    def test_get_users_full_returns_dict_and_key_exists(self):
        result = self.cuc.get_users(mini=False)
        self.assertTrue(isinstance(result, dict)) and 'User' in result

    def test_get_users_mini_returns_list(self):
        result = self.cuc.get_users(mini=True)
        self.assertTrue(isinstance(result, list))

    def test_get_user_call_handler_oid_returns_non_empty_string(self):
        user_oid = self.cuc.get_users(mini=True)[0][2]
        result = self.cuc.get_user_call_handler_oid(user_oid)
        self.assertIsNot(result, '')

    def test_get_user_call_handler_oid_with_unknown_oid_returns_404(self):
        result = self.cuc.get_user('1234567890')
        self.assertEqual(result, 'User not found')

    def test_get_user_returns_schedule_oid(self):
        user_oid = self.cuc.get_users(mini=True)[0][2]
        result = self.cuc.get_user(user_oid)['ObjectId']
        self.assertEqual(result, user_oid)

    def test_get_user_with_unknown_oid_returns_404(self):
        result = self.cuc.get_user('1234567890')
        self.assertEqual(result, 'User not found')

    def test_get_user_pin_settings_returns_user_oid(self):
        user_oid = self.cuc.get_users(mini=True)[0][2]
        result = self.cuc.get_user_pin_settings(user_oid)['UserObjectId']
        self.assertEqual(result, user_oid)

    def test_get_user_pin_settings_with_unknown_oid_returns_404(self):
        result = self.cuc.get_user_pin_settings('1234567890')
        self.assertEqual(result, 'User not found')

    def test_get_user_password_settings_returns_user_oid(self):
        user_oid = self.cuc.get_users(mini=True)[0][2]
        result = self.cuc.get_user_password_settings(user_oid)['UserObjectId']
        self.assertEqual(result, user_oid)

    def test_get_user_password_settings_with_unknown_oid_returns_404(self):
        result = self.cuc.get_user_password_settings('1234567890')
        self.assertEqual(result, 'User not found')

    def test_get_user_templates_returns_list(self):
        result = self.cuc.get_user_templates()
        self.assertTrue(isinstance(result, list))

    def test_get_call_handler_template_oid_returns_non_empty_string(self):
        result = self.cuc.get_call_handler_template_oid()
        self.assertIsNot(result, '')

    def test_get_call_handlers_full_returns_dict_and_key_exists(self):
        result = self.cuc.get_call_handlers(mini=False)
        self.assertTrue(isinstance(result, dict)) and 'Schedule' in result

    def test_get_call_handlers_mini_returns_list(self):
        result = self.cuc.get_call_handlers(mini=True)
        self.assertTrue(isinstance(result, list))

    def test_get_call_handler_returns_call_handler_oid(self):
        call_handler_oid = self.cuc.get_call_handlers(mini=True)[0][1]
        result = self.cuc.get_call_handler(call_handler_oid)['ObjectId']
        self.assertEqual(result, call_handler_oid)

    def test_get_call_handler_with_unknown_oid_returns_404(self):
        result = self.cuc.get_call_handler('1234567890')
        self.assertEqual(result, 'Call handler not found')

    def test_get_call_handler_greeting_returns_invalid_greeting_for_unknown_greeting_type(self):
        call_handler_oid = self.cuc.get_call_handlers(mini=True)[0][1]
        greeting = 'blah'
        result = self.cuc.get_call_handler_greeting(call_handler_oid, greeting=greeting)
        self.assertEqual(result, 'Invalid greeting: {0}'.format(greeting))

    def test_get_call_handler_greetings_returns_list(self):
        call_handler_oid = self.cuc.get_call_handlers(mini=True)[0][1]
        result = self.cuc.get_call_handler_greetings(call_handler_oid)['Greeting']
        self.assertTrue(isinstance(result, list))

    def test_get_call_handler_greetings_with_unknown_oid_returns_404(self):
        result = self.cuc.get_call_handler('1234567890')
        self.assertEqual(result, 'Call handler not found')

    def test_get_call_handler_greeting_with_unknown_oid_returns_404(self):
        result = self.cuc.get_call_handler_greeting('1234567890')
        self.assertEqual(result, 'Call handler not found')

    def test_get_call_handler_greeting_returns_call_handler_oid(self):
        call_handler_oid = self.cuc.get_call_handlers(mini=True)[0][1]
        result = self.cuc.get_call_handler_greeting(call_handler_oid, greeting='Standard')['CallHandlerObjectId']
        self.assertEqual(result, call_handler_oid)

    def test_get_call_handler_greeting_with_off_hours_returns_off_hours_greeting(self):
        call_handler_oid = self.cuc.get_call_handlers(mini=True)[0][1]
        result = self.cuc.get_call_handler_greeting(call_handler_oid, greeting='Off Hours')['GreetingType']
        self.assertEqual(result, 'Off Hours')

    def test_get_caller_input_returns_list(self):
        call_handler_oid = self.cuc.get_call_handlers(mini=True)[0][1]
        result = self.cuc.get_caller_input(call_handler_oid)
        self.assertTrue(isinstance(result, list))

    def test_get_caller_input_with_unknown_oid_returns_404(self):
        result = self.cuc.get_caller_input('1234567890')
        self.assertEqual(result, 'Call handler not found')

    def test_delete_schedule_set_with_invalid_oid_returns_404(self):
        result = self.cuc.delete_schedule_set('1234567890')
        self.assertEqual(result, 'Schedule set not found')

    def test_delete_schedule_with_invalid_oid_returns_404(self):
        result = self.cuc.delete_schedule('1234567890')
        self.assertEqual(result, 'Schedule not found')

    def test_add_schedule_is_successful_and_delete_schedule_successful(self):
        owner_location_oid = self.cuc.get_owner_location_oid()
        result = self.cuc.add_schedule('Test case schedule', owner_location_oid)

        # clean up
        s_del = self.cuc.delete_schedule(result[2])
        ss_del = self.cuc.delete_schedule_set(result[1])

        self.assertEqual(result[0], 'Schedule successfully added') and \
        self.assertEqual(ss_del, 'Schedule set deleted') and \
        self.assertEqual(s_del, 'Schedule deleted')

    def test_update_schedule_is_successful(self):
        owner_location_oid = self.cuc.get_owner_location_oid()
        schedule = self.cuc.add_schedule('Test Case Schedule', owner_location_oid)

        # get holiday schedule oid
        for i in self.cuc.get_schedules():
            if i[0] == 'Holidays':
                holiday_schedule_oid = i[1]

        result = self.cuc.update_schedule_holiday(schedule[1], holiday_schedule_oid)

        #clean up
        self.cuc.delete_schedule(schedule[2])
        self.cuc.delete_schedule_set(schedule[1])

        self.assertEqual(result, 'Schedules holiday schedule successfully updated')

    def test_add_user_is_successful_and_delete_user_is_successful(self):
        result = self.cuc.add_user('Test case user', '77777', 'First Name', 'Last Name', 'Test User Template', '255')

        # clean up
        u_del = self.cuc.delete_user(result[1])

        self.assertEqual(result[0], 'User successfully added') and \
        self.assertEqual(u_del, 'User deleted')

    def test_add_call_handler_is_successful_and_delete_call_handler_is_successful(self):
        call_handler_template_oid = self.cuc.get_call_handler_template_oid()
        owner_location_oid = self.cuc.get_owner_location_oid()
        schedule = self.cuc.add_schedule('Test case call handler schedule', owner_location_oid)

        result = self.cuc.add_call_handler('Test case call handler', '88888', call_handler_template_oid, schedule[1])

        # clean up
        s_del = self.cuc.delete_schedule(schedule[2])
        ss_del = self.cuc.delete_schedule_set(schedule[1])

        self.assertEqual(result[0], 'Call handler added successfully') and \
        self.assertEqual(ss_del, 'Schedule set deleted') and \
        self.assertEqual(s_del, 'Schedule deleted')

