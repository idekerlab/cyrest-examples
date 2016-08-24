# -*- coding: utf-8 -*-
"""
This class has methods to create network object from many data format, delete sessions and get sessions.

"""
import os
import requests
import json
import pandas as pd

from . import HEADERS, SUID_LIST
from ..util import cytoscapejs as util

from ..util import util_networkx as nx_util
from ..util import util_igraph as ig_util
from ..util import dataframe as df_util
from ..util import util_numpy as np_util

JSON = 'json'

from .cynetwork import CyNetwork, check_response

class NetworkClient(object):
    """
    This class has methods to create network object from many data format, delete sessions and get sessions.

    """
    def __init__(self, url, session=None):
        self.__url = url + 'networks'
        # Using a persistent session object, so we don't have to create one for every request.
        self.session = session if session is not None else requests.Session()

    def create_from(self, locations=None, collection=None):
        """
        By using this method, you can load network, session, table and visualize network from url lists.
        You can also set collection parameter to put networks to the collection that you want.

        :param locations: list. You can input local path or url.
        :param collection: string.

        :return : If you input the list of location, you will get list of Cytoscape network objects.
                  If you input the one location, you will get one Cytoscape network object.

        """
        if locations is None:
            raise ValueError('Locations parameter is required.')

        input_type = type(locations)
        if input_type is list or input_type is tuple or input_type is set:
            location_list = []
            for loc in locations:
                if not str(loc).startswith('http'):
                    location_list.append(self.__to_file_url(loc))
                else:
                    location_list.append(loc)
        else:
            if not str(locations).startswith('http'):
                location_list = [self.__to_file_url(locations)]
            else:
                location_list = [locations]

        if collection is None:
            collection_name = 'Created from resources'
        else:
            collection_name = collection

        parameters = {
            'collection': collection_name,
            'source': 'url'
        }

        res = self.session.post(self.__url, data=json.dumps(location_list),
                                params=parameters, headers=HEADERS)
        check_response(res)
        res = res.json()

        if len(res) == 1:
            network_ids = res[0]['networkSUID']
            if len(network_ids) == 1:
                return CyNetwork(network_ids[0], session=self.session,
                                 url=self.__url)
            else:
                return [CyNetwork(suid, session=self.session, url=self.__url) for
                        suid
                        in
                        network_ids]
        else:
            result_dict = {entry['source']: CyNetwork(entry['networkSUID'],
                                                      session=self.session,
                                                      url=self.__url)
                           for entry in res}
            return pd.Series(result_dict)

    def __to_file_url(self, file_name):
        local_file = os.path.abspath(file_name)
        return 'file:///' + local_file

    def create(self, suid=None, name=None, collection=None,
               data=None):
        """
        This method is to create Cytoscape Object from existing network
        and is also to create network by using parameter and then create Cytoscape Object.

        :param suid: If you want to create Cytoscape Object from existing network, you should input the network's suid.
                     On the other hand, if you don't input this parameter, you can make network by using parameter and get that Cytoscape object.
        :param name: The network name. This parameter is only valid when you don't input suid parameter.
        :param collection: The collection name. This parameter is only valid when you don't input suid parameter.
        :param data: The network data and the data format is cytoscape.js. This parameter is only valid when you don't input suid parameter.

        :return : The Cytoscape object.
        """
        if suid is not None:
            # fetch existing network
            res = self.session.get(self.__url)
            existing_networks = res.json()
            if suid in existing_networks:
                network_id = suid
            else:
                raise ValueError('No such network')
        else:
            if data is None:
                network_data = util.get_empty_network()
            else:
                network_data = data

            if name is not None:
                network_data['data']['name'] = name

            if collection is None:
                network_collection = 'From cyREST'
            else:
                network_collection = collection

            res = self.session.post(self.__url + '?collection=' + network_collection,
                                    data=json.dumps(network_data), headers=HEADERS)
            check_response(res)
            result = res.json()
            network_id = result['networkSUID']

        return CyNetwork(network_id, session=self.session, url=self.__url)

    def create_from_networkx(self, network, name=None, collection=None):
        """
        This method create network from networkx. You can use networkx's object, create Cytoscape network and get the Cytoscape Object.

        :param network: The object of networkx.
        :param name: The network name that you will create in Cytoscape.
        :param collection: The collection name.

        :return : Cytoscape object
        """
        if network is None:
            raise ValueError('NetworkX graph object is required.')

        cyjs = nx_util.from_networkx(network)
        return self.create(name=name, collection=collection, data=cyjs)

    def create_from_igraph(self, network, name=None, collection=None):
        """
        This method create network from igraph. You can use igraph's object, create Cytoscape network and get the Cytoscape Object.

        :param network: The object of igraph.
        :param name: The network name that you will create in Cytoscape.
        :param collection: The collection name.

        :return : Cytoscape object
        """
        if network is None:
            raise ValueError('igraph object is required.')

        cyjs = ig_util.from_igraph(network)
        return self.create(name=name, collection=collection, data=cyjs)

    def create_from_ndarray(self, matrix, name=None, labels=None,
        collection=None, weighted=False):
        """
        This method create network from igraph. You can use igraph's object, create Cytoscape network and get the Cytoscape Object.

        :param matrix: ndarray data.
        :param name: The network name.
        :param labels: The labels
        :param collection: The collection name
        :param weighted: If this value is True, the edges will be weighted.
                         If this value is False, The edges will be unweighted.

        :return : Cytoscape obejct.
        """
        if matrix is None:
            raise ValueError('2D ndarray object is required.')

        cyjs = np_util.from_ndarray(matrix, name, labels, weighted=weighted)
        return self.create(name=name, collection=collection, data=cyjs)

    def create_from_dataframe(self, dataframe, source_col='source',
                              target_col='target', interaction_col='interaction',
                              name='Created from DataFrame', collection=None):
        """
        This method create network from Pandas DataFrame.
        You can use Pandas DataFrame's object, create Cytoscape network and get the Cytoscape Object.

        :param dataframe: the network data
        :param source_col: the source column name in data frame.
        :param target_col: the target column name in data frame.
        :param interaction_col: the interaction column name in data frame.
        :param name: the network name that you will create from data frame.
        :param collection: The collection name.

        :return : The cytoscape object.
        """
        if dataframe is None:
            raise ValueError('DataFrame object is required.')

        # Convert from DataFrame to Cytoscape.js JSON
        cyjs = df_util.from_dataframe(dataframe, source_col=source_col,
                              target_col=target_col, interaction_col=interaction_col,
                              name=name)
        return self.create(collection=collection, data=cyjs)

    def get_all(self, format=SUID_LIST):
        """
        You can get the all of the network session. You can get the value as SUID list or JSON.

        :param format: The default value is SUID_LIST. You can also set this parameter as JSON.

        :return : the all session
        """
        if format is SUID_LIST:
            result = self.session.get(self.__url)
        elif format is JSON:
            result = self.session.get(self.__url + '.json')
        else:
            raise ValueError('Unsupported format type: ' + format)

        return result.json()

    def get(self, id):
        """
        You can set network id and get the network session information.

        :param id: the network id

        :return : the session as JSON format.
        """
        return self.session.get(self.__url + '/' + str(id)).json()

    def delete_all(self):
        """
        Delete all network session.

        """
        self.session.delete(self.__url)

    def delete(self, cynetwork):
        """
        Delete network session that you want by sessing cynetwork object which will be deleted.

        :param cynetwork: The cynetwork that you want to delete session.
        """
        id = cynetwork.get_id()
        self.session.delete(self.__url + '/' + str(id))
        del cynetwork
