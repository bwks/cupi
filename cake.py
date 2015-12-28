import json
import requests


class CUPI(object):
    """
    CUPI class, main class for configuring Cisco Unity

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
        self.cuc.headers.update({'Accept': 'application/json', 'Connection': 'keep_alive'})

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





