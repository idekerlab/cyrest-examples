# -*- coding: utf-8 -*-
"""

"""
from . import BASE_URL, HEADERS
import requests
import json
import pandas as pd


class Style(object):
    """

    """
    def __init__(self, name):
        # Validate required argument
        if name is None:
            raise ValueError("Style name is required.")
        else:
            self.__name = name

        self.__url = BASE_URL + 'styles/' + str(name) + '/'

    def get_name(self):
        """
        Get immutable name of this Visual Style.

        :return: Style name as string
        """
        return self.__name

    def __get_new_mapping(self, mapping_type, column=None, col_type='String',
                          vp=None):
        if column is None or vp is None:
            raise ValueError('both column name and visual property are required.')

        new_maping = {
            'mappingType': mapping_type,
            'mappingColumn': column,
            'mappingColumnType': col_type,
            'visualProperty': vp
        }

        return new_maping

    def create_discrete_mapping(self, column=None, col_type='String',
                                vp=None, mappings=None):
        """
        Create discrete mapping. By this method, you can create discrete mapping with some column's value and view.

        :param column: The table's column name.
        :param col_type: The table's column type.
        :param vp: The visual proparty
        :param mappings : This is the python's dictionary value. The key is the descrete column's value and value is that column's value.
        """
        self.__call_create_mapping(
            self.__get_discrete(column=column, col_type=col_type, vp=vp,
                                mappings=mappings))

    def create_continuous_mapping(self, column=None, col_type='String',
                                  vp=None, points=None):
        """
        Create continuous mapping. By this method, you can create continuous mapping with some column's value and view.

        :param column: The table's column name.
        :param col_type: The table's column type.
        :param vp: The visual proparty
        :param points: the points. You can create this value by create_slope and create_2_color_gradient that are StyleUtil class's methods in py2cytoscape.data.style
        """
        self.__call_create_mapping(
            self.__get_continuous(column=column, col_type=col_type, vp=vp,
                                  points=points))

    def create_passthrough_mapping(self, column=None, col_type='String',
                                   vp=None):
        """
        Create pass through mapping. By using this method, you can set value from table to view.

        :param column: The table's column name.
        :param col_type: The column type.
        :param vp: vizual proparty.

        """
        self.__call_create_mapping(
            self.__get_passthrough(column=column, col_type=col_type, vp=vp))

    def __call_create_mapping(self, mapping):
        url = self.__url + 'mappings'
        requests.post(url, data=json.dumps([mapping]), headers=HEADERS)

    def __get_passthrough(self, column=None, col_type='String', vp=None):
        return self.__get_new_mapping('passthrough', column=column,
                                      col_type=col_type, vp=vp)

    def __get_discrete(self, column=None, col_type='String', vp=None,
                       mappings=None):
        new_mapping = self.__get_new_mapping('discrete', column=column,
                                             col_type=col_type, vp=vp)
        if mappings is None:
            raise ValueError('key-value pair object (mappings) is required.')
        body = [{'key': key, 'value': mappings[key]} for key in mappings.keys()]
        new_mapping['map'] = body
        return new_mapping

    def __get_continuous(self, column=None, col_type='String', vp=None,
                         points=None):
        if points is None:
            raise ValueError('key-value pair object (mappings) is required.')
        new_mapping = self.__get_new_mapping('continuous', column=column,
                                             col_type=col_type, vp=vp)
        new_mapping['points'] = points
        return new_mapping

    def get_mapping(self, vp=None):
        """
        :param vp:
        :return :
        """
        if vp is None:
            raise ValueError('Visual Property ID is required.')

        url = self.__url + 'mappings/' + vp
        return requests.get(url).json()

    def get_mappings(self):
        """
        :return :
        """
        url = self.__url + 'mappings'
        return requests.get(url).json()

    def get_default(self, vp=None):
        """
        :param vp:
        :return :
        """
        if vp is None:
            raise ValueError('Visual Property ID is required.')

        url = self.__url + 'defaults/' + vp
        key_value_pair = requests.get(url).content
        print(key_value_pair)
        key2 = requests.get(url).json()
        key_value_pair = key2
        return pd.Series({key_value_pair['visualProperty']: key_value_pair[
            'value']})

    def get_defaults(self):
        """
        :return :
        """
        url = self.__url + 'defaults'
        result = requests.get(url).json()['defaults']
        vals = {entry['visualProperty']: entry['value'] for entry in result}
        return pd.Series(vals)

    def update_defaults(self, key_value_pair):
        """
        :param key_value_pair:
        """
        body = []
        for key in key_value_pair:
            entry = {
                'visualProperty': key,
                'value': key_value_pair[key]
            }
            body.append(entry)

        url = self.__url + 'defaults'
        requests.put(url, data=json.dumps(body), headers=HEADERS)

    # Delete Methods

    def delete_mapping(self, vp=None):
        """
        :param vp:
        """
        if vp is None:
            return

        url = self.__url + 'mappings/' + vp
        requests.delete(url)

    def delete_mappings(self):
        """
        """
        url = self.__url + 'mappings'
        requests.delete(url)


class StyleUtil(object):
    """
    """

    @staticmethod
    def create_2_color_gradient(min=0, max=10, colors=('red', 'green')):
        """
        create
        :param min:
        :param max:
        :param colors:
        :return :
        """
        points = [
            {
                'value': str(min),
                'lesser': colors[0],
                'equal':  colors[0],
                'greater': colors[0],
            },
            {
                'value': str(max),
                'lesser': colors[1],
                'equal': colors[1],
                'greater': colors[1]
            }
        ]

        return points

    @staticmethod
    def create_slope(min=0, max=10, values=(1, 10)):
        """
        :param min:
        :param max:
        :param values:
        :return :
        """

        points = [
            {
                'value': str(min),
                'lesser': values[0],
                'equal':  values[0],
                'greater': values[0],
            },
            {
                'value': str(max),
                'lesser': values[1],
                'equal': values[1],
                'greater': values[1]
            }
        ]

        return points
