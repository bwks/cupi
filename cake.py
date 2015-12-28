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
        Init sets up the connection to Cisco Unity Connection

        :param cuc: Unity connection IP Address
        :param username: User with privilege to access rest api
        :param password: Users password
        """
        self.url_base = 'https://{0}/vmrest/'.format(cuc)
        self.cuc = requests.session()
        self.cuc.auth = (username, password)
        self.cuc.verify = False
        self.cuc.headers.update({'Accept': 'application/json', 'Connection': 'keep_alive'})

    def get_owner_location_oid(self):
        """
        Get the owner location oid. This is needed for creating schedules
        :return: owner location oid
        """
        url = '{0}locations/connectionlocations'.format(self.url_base)
        return self.cuc.get(url).json()['ConnectionLocation']['ObjectId']

    def get_call_handler_template_oid(self):
        """
        Method to get the call handler template oid
        :return: call handler template oid
        """
        url = '{0}callhandlertemplates'.format(self.url_base)
        return self.cuc.get(url).json()['CallhandlerTemplate']['ObjectId']



