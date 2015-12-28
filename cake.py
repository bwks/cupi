"""
Class to interface with cisco unity connection cupi api.
Author: Brad Searle
Version: 0.1
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

    def add_schedule(self, display_name, owner_location_oid):
        """

        :param display_name:
        :param owner_location_oid:
        :return:
        """

        body = {
            'DisplayName': display_name,
            'OwnerLocationObjectId': owner_location_oid,
        }
        url = '{0}/schedulesets'.format(self.url_base)

        resp = self.cuc.post(url, body=body)
        schedule_set_oid = resp.text.split('/')[-1]

        return schedule_set_oid


