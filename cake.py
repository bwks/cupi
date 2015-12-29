"""
Class to interface with cisco unity connection cupi api.
Author: Brad Searle
Version: 0.2
"""

import json

import requests


class CUPI(object):
    """
    Class for configuring Cisco Unity

    example usage:
    >>> from cupi.cake import CUPI
    >>> c = CUPI('192.168.200.11', 'username', 'password')
    >>> c.get_owner_location_oid()
    >>> '89443b75-0547-4008-8245-39c3abeaed31'
    """

    def __init__(self, cuc, username, password):
        """
        Sets up the connection to Cisco Unity Connection

        :param cuc: Unity connection IP Address
        :param username: User with privilege to access rest api
        :param password: Users password
        """

        self.url_base = 'https://{0}/vmrest'.format(cuc)
        self.cuc = requests.session()
        self.cuc.auth = (username, password)
        self.cuc.verify = False
        self.cuc.headers.update({
            'Accept': 'application/json',
            'Connection': 'keep_alive',
            'Content_type': 'application/json',
        })

    def get_owner_location_oid(self):
        """
        Get the owner location oid. This is needed for creating schedules
        :return: owner location oid
        """

        url = '{0}/locations/connectionlocations'.format(self.url_base)
        return self.cuc.get(url).json()['ConnectionLocation']['ObjectId']

    def get_call_handler_template_oid(self):
        """
        Method to get the call handler template oid
        :return: call handler template oid
        """

        url = '{0}/callhandlertemplates'.format(self.url_base)
        return self.cuc.get(url).json()['CallhandlerTemplate']['ObjectId']

    def get_user_call_handler_oid(self, user_oid):
        """
        Get the oid of a call handler assigned to a user
        :param user_oid: oid of the user to get the call handler oid
        :return: users call handler oid
        """

        url = '{0}/users/{1}'.format(self.url_base, user_oid)
        return self.cuc.get(url).json()['CallHandlerObjectId']

    def get_users(self):
        """
        Get all users
        :return: A list of user dictionaries
        """

        url = '{0}/users'.format(self.url_base)
        return self.cuc.get(url).json()['User']

    def get_user_templates(self):
        """
        Get user templates, used when adding users
        :return: a list of tuples of user template alias's and oid's
        """

        url = '{0}/usertemplates'.format(self.url_base)
        resp = self.cuc.get(url).json()

        if resp['@total'] == '1':
            # if there is only one result the response will not be in a list
            return resp['UserTemplate']['Alias'], resp['UserTemplate']['ObjectId']
        else:
            return [(i['Alias'], i['ObjectId']) for i in resp['UserTemplate']]

    def get_schedule_sets(self, mini=True):
        """
        Get Schedule Sets
        :param mini: return minimal list if True else return full json response
        :return: a list of tuples of schedule sets
        """

        url = '{0}/schedulesets'.format(self.url_base)
        resp = self.cuc.get(url).json()

        if mini:
            return [(i['DisplayName'], i['ObjectId']) for i in resp['ScheduleSet']]
        else:
            return resp

    def get_schedules(self, mini=True):
        """
        Get Schedules
        :param mini: return minimal list if True else return full json response
        :return: a list of tuples of schedules
        """

        url = '{0}/schedules'.format(self.url_base)
        resp = self.cuc.get(url).json()

        if mini:
            return [(i['DisplayName'], i['ObjectId']) for i in resp['Schedule']]
        else:
            return resp

    def add_schedule(self,
                     display_name,
                     owner_location_oid,
                     is_holiday='false',
                     start_time='510',
                     end_time='1020',
                     is_active_monday='true',
                     is_active_tuesday='true',
                     is_active_wednesday='true',
                     is_active_thursday='true',
                     is_active_friday='true',
                     is_active_saturday='false',
                     is_active_sunday='false'):
        """
        To add a schedule there are 4 steps
        1) Add a schedule set
        2) Add a schedule
        3) Map the schedule to the scheduleset with a schedule set map
        4) Add a schedule detail to the schedule
        Default schedule times are Monday - Friday 8.30am - 5.00pm
        :param display_name: Schedule display name
        :param owner_location_oid: Get this oid with the get_owner_location_oid method
        :param is_holiday: Is this schedule a holiday schedule true/false
        :param start_time: Schedule start time
        :param end_time: Schedule end time
        :param is_active_monday: Schedule active Monday true/false
        :param is_active_tuesday: Schedule active Tuesday true/false
        :param is_active_wednesday: Schedule active Wednesday true/false
        :param is_active_thursday: Schedule active Thursday true/false
        :param is_active_friday: Schedule active Friday true/false
        :param is_active_saturday: Schedule active Saturday true/false
        :param is_active_sunday: Schedule active Sunday true/false
        :return: Result of adding the schedule

        example usage:
                                    display_name                         owner_location_oid
        >>> c.add_schedule('test_schedule M-F 8.30am - 5.00pm', '89443b75-0547-4008-8245-39c3abeaed31')
        >>> 'Schedule Successfully Added'
        """

        # 1) Add a schedule set
        url = '{0}/schedulesets'.format(self.url_base)
        body = {
            'DisplayName': display_name,
            'OwnerLocationObjectId': owner_location_oid,
        }

        resp = self.cuc.post(url, json=body)
        schedule_set_oid = resp.text.split('/')[-1]
        print(schedule_set_oid)

        if resp.status_code != 201:
            return 'Could not add schedule set {0} {1}'.format(resp.status_code, resp.reason)

        # 2) Add a schedule
        else:
            url = '{0}/schedules'.format(self.url_base)
            body = {
                'DisplayName': display_name,
                'OwnerLocationObjectId': owner_location_oid,
                'IsHoliday': is_holiday
            }

            resp = self.cuc.post(url, json=body)
            schedule_oid = resp.text.split('/')[-1]
            print(schedule_oid)

            if resp.status_code != 201:
                return 'Could not add schedule {0} {1}'.format(resp.status_code, resp.reason)

            # 3) Map the schedule to the schedule set with a schedule set map
            else:
                url = '{0}/schedulesets/{1}/schedulesetmembers'.format(self.url_base, schedule_set_oid)
                body = {
                    'ScheduleSetObjectId': schedule_set_oid,
                    'ScheduleObjectId': schedule_oid,
                    'Exclude': 'false'
                }

                resp = self.cuc.post(url, json=body)

                if resp.status_code != 201:
                    return 'Could not map schedule to schedule set {0} {1}'.format(resp.status_code, resp.reason)

                # 4) Add a schedule detail to the schedule
                else:
                    url = '{0}/schedules/{1}/scheduledetails'.format(self.url_base, schedule_oid)
                    body = {
                        'Subject': display_name,
                        'StartTime': start_time,
                        'EndTime': end_time,
                        'IsActiveMonday': is_active_monday,
                        'IsActiveTuesday': is_active_tuesday,
                        'IsActiveWednesday': is_active_wednesday,
                        'IsActiveThursday': is_active_thursday,
                        'IsActiveFriday': is_active_friday,
                        'IsActiveSaturday': is_active_saturday,
                        'IsActiveSunday': is_active_sunday,
                    }

                    resp = self.cuc.post(url, json=body)

                    if resp.status_code != 201:
                        return 'Could not add schedule detail {0} {1}'.format(resp.status_code, resp.reason)

                    else:
                        return 'Schedule Successfully Added'

    def delete_schedule_set(self, schedule_set_oid):
        """

        :param schedule_set_oid:
        :return:
        """

        url = '{0}/schedulesets/{1}'.format(self.url_base, schedule_set_oid)

        resp = self.cuc.delete(url)
        if resp.status_code == 204:
            return 'Schedule set deleted'
        elif resp.status_code == 404:
            return 'Schedule set not found'
        else:
            return 'Unknown Result {0} {1}'.format(resp.status_code, resp.reason)

    def delete_schedule(self, schedule_oid):
        """

        :param schedule_oid:
        :return:
        """

        url = '{0}/schedules/{1}'.format(self.url_base, schedule_oid)

        resp = self.cuc.delete(url)
        if resp.status_code == 204:
            return 'Schedule deleted'
        elif resp.status_code == 404:
            return 'Schedule not found'
        else:
            return 'Unknown Result {0} {1}'.format(resp.status_code, resp.reason)