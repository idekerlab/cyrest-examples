# -*- coding: utf-8 -*-
"""
This is the most important and most basic class to use cytoscape programatically.

"""
import requests
from .network_client import NetworkClient
from .style_client import StyleClient
from .algorithm_client import LayoutClient
from .algorithm_client import EdgeBundlingClient
from .session_client import SessionClient

from . import PORT, IP, VERSION


class CyRestClient(object):
    """
    This class is the most basic class to use Cytoscape programatically.
    In this class, you can use all methods to controll Cytoscape.

    So, if you want to use py2cytoscape, the first step is to call this class.
    """

    def __init__(self, ip=IP, port=PORT, version=VERSION):
        self.__url = 'http://' + ip + ':' + str(port) + '/' + version + '/'

        self.network = NetworkClient(self.__url)
        self.style = StyleClient(self.__url)
        self.layout = LayoutClient(self.__url)
        self.edgebundling = EdgeBundlingClient(self.__url)
        self.session = SessionClient(self.__url)

    def status(self):
        """
        Using this method, you can check whether the status of connection to cyREST is stable or not.
        """
        try:
            response = requests.get(self.__url).json()
        except Exception as e:
            print('Could not get status from cyREST: ' + e)
        else:
            return response
