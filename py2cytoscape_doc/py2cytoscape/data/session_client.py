# -*- coding: utf-8 -*-
"""

"""
import requests


class SessionClient(object):
    """
    This class is managing session. You can delete, save and open session by this class's methods.

    """
    def __init__(self, url):
        self.__url = url + 'session'

    def delete(self):
        """
        This method is to delete current session and start new one.
        """
        requests.delete(self.__url)

    def save(self, file_name=None):
        """
        This method is save the session.

        :param file_name: the file name
        :return : the session status.
        """
        if file_name is None:
            raise ValueError('Session file name is required.')

        post_url = self.__url
        params = {'file': file_name}
        res = requests.post(post_url, params=params)
        return res

    def open(self, file_name=None):
        """
        :param file_name: the file name that you want to open.
        :return :  
        """
        if file_name is None:
            raise ValueError('Session file name is required.')

        get_url = self.__url
        params = {'file': file_name}
        res = requests.get(get_url, params=params)
        return res
