# -*- coding: utf-8 -*-
"""

"""
from py2cytoscape.data.base_view import BaseView

import requests
import json

from . import HEADERS


class NodeView(BaseView):
    """
    In this class, we can 
    """
    # Utility Methods to access node position
    def get_x(self):
        """
        Get the NODE_X_LOCATION visual propaties.

        :return : the value of NODE_X_LOCATION
        """
        return self.get_value('NODE_X_LOCATION')

    def get_y(self):
        """
        Cet the NODE_Y_LOCATION visual propaties.

        :return : the value of NODE_Y_LOCATION
        """
        return self.get_value('NODE_Y_LOCATION')

    def set_x(self, x):
        """
        Set the visual propatity value of NODE_X_LOCATION

        :param x: NODE_X_LOCATION's value
        """
        self.set_value('NODE_X_LOCATION', x)
