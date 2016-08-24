# -*- coding: utf-8 -*-
"""
CyNetwork class is a simple wrapper for network-related cyREST raw REST API.
It does not hold the actual network data. It's a reference to a network in current Cytoscape session.

With CyNetwork API, you can access Cytoscape data objects in more Pythonista-friendly way.
"""
import json

import pandas as pd
import requests
from py2cytoscape.data.network_view import CyNetworkView

from ..util import util_networkx as nx_util
from ..util import dataframe as df_util

from . import BASE_URL, HEADERS

BASE_URL_NETWORK = BASE_URL + 'networks'


class CyNetwork(object):
    """
    
    """
    def __init__(self, suid=None, session=None, url=None):
        if pd.isnull(url):
            raise ValueError("URL is missing.")
        # Validate required argument
        if pd.isnull(suid):
            raise ValueError("SUID is missing.")
        else:
            self.__id = suid

        self.__url = url + '/' + str(self.__id) + '/'
        self.session = session if session is not None else requests.Session()

    def get_id(self):
        """
        Get session-unique ID of this network

        :return: SUID as integer
        """
        return self.__id

    def to_json(self):
        """
        Return this network in Cytoscape.js format.

        :return: Cytoscape.js Style JSON as dictionary.
        """
        return self.session.get(self.__url).json()

    def to_networkx(self):
        """
        Return this network in NetworkX graph object.

        :return: Network as NetworkX graph object
        """
        return nx_util.to_networkx(self.session.get(self.__url).json())

    def to_dataframe(self):
        """
        Return this network in pandas DataFrame.

        :return: Network as DataFrame.  This is equivalent to SIF.
        """
        return df_util.to_dataframe(self.session.get(self.__url).json())

    def get_nodes(self):
        """
        Get all nodes as a list of SUIDs

        :return:
        """
        return self.session.get(self.__url + 'nodes').json()

    def get_edges(self, format='suid'):
        """
        Get edges as a json format.

        :param format: Now the 'suid' format is only available.
        :return: If the method's input is 'suid', then this method returns the edges with json format.
        """
        if format is 'suid':
            return self.session.get(self.__url + 'edges').json()
        elif format is 'edgelist':
            # TODO: implement this
            pass
        else:
            raise ValueError(format + ' is not supported for edge format.')

    def add_node(self, node_name, dataframe=False):
        """
        Add a single node to the network.

        :param node_name: the node name that you want to get.
        :param dataframe: The default value is False. If True, return a pandas dataframe instead of a dict.

        :return : A dict mapping names to SUIDs for the newly-created nodes. If node_name is 'None', the return is 'None'.
        """
        if node_name is None:
            return None
        return self.add_nodes([node_name], dataframe=dataframe)

    def add_nodes(self, node_name_list, dataframe=False):
        """
        Add new nodes to the network

        :param node_name_list: list of node names, e.g. ['a', 'b', 'c']
        :param dataframe: If True, return a pandas dataframe instead of a dict.

        :return: A dict mapping names to SUIDs for the newly-created nodes.
        """
        res = self.session.post(self.__url + 'nodes', data=json.dumps(node_name_list), headers=HEADERS)
        check_response(res)
        nodes = res.json()
        if dataframe:
            return pd.DataFrame(nodes).set_index(['SUID'])
        else:
            return {node['name']: node['SUID'] for node in nodes}

    def add_edge(self, source, target, interaction='-', directed=True, dataframe=True):
        """
        Add a single edge from source to target.

        :param source: String. This is the source node name.
        :param target: String. This is the target node name.
        :param interaction:
        :param directed: You can choose this edge is directed or not. The default value is True.
        :param dataframe: If dataframe is True (default), return a Pandas DataFrame.
                          If dataframe is False, return a list of dicts with keys 'SUID', 'source' and 'target'.

        :return : If parameter:dataframe is True (default), return a Pandas DataFrame.
                  If parameter:dataframe is False, return a list of dicts with keys 'SUID', 'source' and 'target'.

        """
        new_edge = {
            'source': source,
            'target': target,
            'interaction': interaction,
            'directed': directed
        }
        return self.add_edges([new_edge], dataframe=dataframe)

    def add_edges(self, edge_list, dataframe=True):
        """
        Add a all edges in edge_list.

        :return: A data structure with Cytoscape SUIDs for the newly-created edges.

        :param edge_list: List of (source, target, interaction) tuples *or*
                          list of dicts with 'source', 'target', 'interaction', 'direction' keys.
        :param dataframe: If dataframe is True (default), return a Pandas DataFrame.
                          If dataframe is False, return a list of dicts with keys 'SUID', 'source' and 'target'.

        :return : If parameter:dataframe is True (default), return a Pandas DataFrame.
                  If parameter:dataframe is False, return a list of dicts with keys 'SUID', 'source' and 'target'.
        """
        # It might be nice to have an option pass a list of dicts instead of list of tuples
        if not isinstance(edge_list[0], dict):
            edge_list = [{'source': edge_tuple[0],
                          'target': edge_tuple[1],
                          'interaction': edge_tuple[2]}
                         for edge_tuple in edge_list]
        res = self.session.post(self.__url + 'edges', data=json.dumps(edge_list), headers=HEADERS)
        check_response(res)
        edges = res.json()
        if dataframe:
            return pd.DataFrame(edges).set_index(['SUID'])
        else:
            return edges

    def delete_node(self, id):
        """
        Delete node.

        :param id: the node id.
        """
        url = self.__url + 'nodes/' + str(id)
        self.session.delete(url)

    def delete_edge(self, id):
        """
        Delete edge.

        :param id: the edge id.
        """
        url = self.__url + 'edges/' + str(id)
        self.session.delete(url)

    def __get_table(self, type, format=None):
        """
        This method return the table data. You can get node or edge table data by using this.
        Cytoscape has two main data types: Network and Table.
        Network is the graph topology, and Tables are properties for those graphs.
        For simplicity, this method has access to three basic table objects.

        :param type: If the value is 'node', this method return node table.
                     On the other hand, if the value is 'edge', this method return edge table.

        :param format: You can choose data format from these: TSV,CSV,cytoscapejs.
                       If the value of format is None, dataframe or tsv, the return format is TSV.
                       If the value of format is csv, the return value is csv.
                       If the value of format is cytoscapejs, the return value is Cytoscape.js style JSON.

        :return : If the value of format is None, dataframe or tsv, the return format is TSV.
                  If the value of format is csv, the return value is csv.
                  If the value of format is cytoscapejs, the return value is Cytoscape.js style JSON.


        """
        url = self.__url + 'tables/default' + type
        if format is None or format is 'dataframe':
            uri = url + '.tsv'
            return pd.read_csv(uri, sep='\t', index_col=0, header=0)
        elif format is 'csv' or format is 'tsv':
            return self.session.get(url + '.' + format).content
        elif format is 'cytoscapejs':
            return self.session.get(url).json()['rows']
        else:
            raise ValueError('Unsupported format: ' + format)

    def get_node_table(self, format=None):
        """
        Get node table.

        Cytoscape has two main data types: Network and Table.
        Network is the graph topology, and Tables are properties for those graphs.
        For simplicity, this method has access to three basic node table objects.

        :param format: You can choose data format from these: TSV,CSV,cytoscapejs.
                       If the value of format is None, dataframe or tsv, the return format is TSV.
                       If the value of format is csv, the return value is csv.
                       If the value of format is cytoscapejs, the return value is Cytoscape.js style JSON.

        :return : If the value of format is None, dataframe or tsv, the return format is TSV.
                  If the value of format is csv, the return value is csv.
                  If the value of format is cytoscapejs, the return value is Cytoscape.js style JSON.
        """
        return self.__get_table('node', format)

    def get_edge_table(self, format=None):
        """
        Get edge table.

        Cytoscape has two main data types: Network and Table.
        Network is the graph topology, and Tables are properties for those graphs.
        For simplicity, this method has access to three basic edge table objects.

        :param format: You can choose data format from these: TSV,CSV,cytoscapejs.
                       If the value of format is None, dataframe or tsv, the return format is TSV.
                       If the value of format is csv, the return value is csv.
                       If the value of format is cytoscapejs, the return value is Cytoscape.js style JSON.

        :return : If the value of format is None, dataframe or tsv, the return format is TSV.
                  If the value of format is csv, the return value is csv.
                  If the value of format is cytoscapejs, the return value is Cytoscape.js style JSON.
        """
        return self.__get_table('edge', format)

    def get_network_table(self, format=None):
        """
        Get network table.

        Cytoscape has two main data types: Network and Table.
        Network is the graph topology, and Tables are properties for those graphs.
        For simplicity, this method has access to three basic network table objects.

        :param format: You can choose data format from these: TSV,CSV,cytoscapejs.
                       If the value of format is None, dataframe or tsv, the return format is TSV.
                       If the value of format is csv, the return value is csv.
                       If the value of format is cytoscapejs, the return value is Cytoscape.js style JSON.

        :return : If the value of format is None, dataframe or tsv, the return format is TSV.
                  If the value of format is csv, the return value is csv.
                  If the value of format is cytoscapejs, the return value is Cytoscape.js style JSON.

        """
        return self.__get_table('network', format)

    def __get_columns(self, type=None):
        url = self.__url + 'tables/default' + type + '/columns'
        df = pd.DataFrame(self.session.get(url).json())
        return df.set_index(['name'])

    def get_node_columns(self):
        """
        Get node table columns information as DataFrame

        :return: Node columns information ad DataFrame
        """
        return self.__get_columns('node')

    def get_edge_columns(self):
        """
        Get edge table columns information as DataFrame

        :return: Edge columns information ad DataFrame
        """
        return self.__get_columns('edge')

    def get_network_columns(self):
        """
        Get network table columns information as DataFrame

        :return: Network columns information as DataFrame
        """
        return self.__get_columns('networks')

    def __get_column(self, type=None, column=None):
        url = self.__url + 'tables/default' + type + '/columns/' + column
        result = self.session.get(url).json()
        return pd.Series(result['values'])

    def get_node_column(self, column):
        """
        Get node table column information as DataFrame

        :param column: you can choose column that you want to get.

        :return : Node column imformation as DataFrame
        """
        return self.__get_column('node', column=column)

    def get_edge_column(self, column):
        """
        Get edge table column information as DataFrame

        :param column: you can choose column that you want to get.

        :return : edge column imformation as DataFrame
        """
        return self.__get_column('edge', column=column)

    def __get_value(self, type=None, id=None, column=None):
        if column is None and id is not None:
            # Extract a row in table
            url = self.__url + 'tables/default' + type + '/rows/' + str(id)
            return pd.Series(self.session.get(url).json())
        elif column is not None and id is not None:
            url = self.__url + 'tables/default' + type + '/rows/' + str(id) + '/' + column
            return self.session.get(url).content
        else:
            raise ValueError('ID is required.')

    def get_node_value(self, id, column=None):
        """
        Get node value information.

        :param id: the node id.
        :param column: input column that you want to get. If you input value in this parameter,
                       you can get all columns' information about node.

        :return : node value information
        """
        return self.__get_value(type='node', id=id, column=column)

    def get_edge_value(self, id, column=None):
        """
        Get edge value information.

        :param id: the edge id.
        :param column: input column that you want to get. If you input value in this parameter,
                       you can get all columns' information about edge.

        :return : edge value information
        """
        return self.__get_value(type='edge', id=id, column=column)

    def get_network_value(self, column):
        """
        Get network value information.

        :param column: input column that you want to get. If you input value in this parameter,
                       you can get all columns' information about network.

        :return : network value information
        """
        return self.__get_value(type='network', id=self.__id, column=column)

    def update_node_table(self, df=None, network_key_col='name',
                          data_key_col=None):
        """
        TODO
        :param df:
        :param network_key_col:
        :param data_key_col:
        :return :
        """
        return self.__update_table('node', df=df, network_key_col=network_key_col, data_key_col=data_key_col)

    def __update_table(self, type, df, network_key_col='name',
                       data_key_col=None):

        is_index_col = False

        if data_key_col is None:
            # Use index
            data_key = network_key_col
            is_index_col = True
        else:
            data_key = data_key_col

        table = {
            'key': network_key_col,
            'dataKey': data_key
        }

        if is_index_col:
            # Use DataFrame's index as the mapping key
            df2 = pd.DataFrame(df)
            df2[network_key_col] = df.index
            data = df2.to_json(orient='records')
            del df2
        else:
            data = df.to_json(orient='records')

        table['data'] = json.loads(data)

        url = self.__url + 'tables/default' + type
        self.session.put(url, json=table, headers=HEADERS)

    def __delete_column(self, type, column):
        url = self.__url + 'tables/default' + type + '/columns/' + column
        self.session.delete(url)

    def delete_node_table_column(self, column):
        """
        Delete node table column that you want to delete.

        :param column: the column that you want to delete.
        """
        self.__delete_column('node', column=column)

    def delete_edge_table_column(self, column):
        """
        Delete edge table column that you want to delete.

        :param column: the column that you want to delete.
        """
        self.__delete_column('edge', column=column)

    def delete_network_table_column(self, column):
        """
        Delete network table column that you want to delete.

        :param column: the column that you want to delete.
        """
        self.__delete_column('network', column=column)

    def __create_column(self, type, name, data_type, immutable, list):
        url = self.__url + 'tables/default' + type + '/columns'
        new_column = {
            'name': name,
            'type': data_type,
            'immutable': immutable,
            'list': list
        }
        self.session.post(url, data=json.dumps(new_column), headers=HEADERS)

    def create_node_column(self, name, data_type='String', is_immutable=False, is_list=False):
        """
        Create new node column.

        :param name: This is the column name.
        :param data_type: This is the column data type. The default value is 'String'. If you want to change type, you put type.
        :param is_immutable: The default value is 'False'. If you want to set this clumn's value as immutable, you input 'True' in this parameter.
        :param is_list: The default value is 'False'
        """
        self.__create_column('node', name=name, data_type=data_type, immutable=is_immutable, list=is_list)

    def create_edge_column(self, name, data_type='String', is_immutable=False, is_list=False):
        """
        Create new edge column.

        :param name: This is the column name.
        :param data_type: This is the column data type. The default value is 'String'. If you want to change type, you put type.
        :param is_immutable: The default value is 'False'. If you want to set this clumn's value as immutable, you input 'True' in this parameter.
        :param is_list: The default value is 'False'
        """
        self.__create_column('edge', name=name, data_type=data_type, immutable=is_immutable, list=is_list)

    def create_network_column(self, name, data_type='String', is_immutable=False, is_list=False):
        """
        Create new network column.

        :param name: This is the column name.
        :param data_type: This is the column data type. The default value is 'String'. If you want to change type, you put type.
        :param is_immutable: The default value is 'False'. If you want to set this clumn's value as immutable, you input 'True' in this parameter.
        :param is_list: The default value is 'False'
        """
        self.__create_column('network', name=name, data_type=data_type, immutable=is_immutable, list=is_list)


    # Utility functions
    def get_neighbours(self, node_id):
        """
        Get the node's neighbours.

        :param node_id: the node id that you want to focus.

        :return : the json value of neighbors' node.
        """
        url = self.__url + 'nodes/' + str(node_id) + '/neighbors'
        return self.session.get(url).json()

    def get_adjacent_edges(self, node_id):
        """
        Get node's adjacent edges that you want to get.

        :param node_id: the node id that you want to focus.
        :return :the json value of adjacent edges.
        """
        url = self.__url + 'nodes/' + str(node_id) + '/adjEdges'
        return self.session.get(url).json()


    # Views
    def get_views(self):
        """
        Get views as a list of SUIDs

        :return:
        """
        url = self.__url + 'views'
        return self.session.get(url).json()

    def get_png(self, height=1200):
        """
        Get the graph as png image.

        :param height: The default height is 1200.

        :return : The object image of png.
        """
        url = self.__url + 'views/first.png?h=' + str(height)
        return self.session.get(url).content

    def get_svg(self, height=1200):
        """
        Get the graph as svg image.

        :param height: The default height is 1200.

        :return : The object image of svg.
        """
        url = self.__url + 'views/first.svg?h=' + str(height)
        return self.session.get(url).content

    def get_pdf(self):
        """
        Get the graph as pdf image.

        :return : The object image of png.
        """
        url = self.__url + 'views/first.pdf'
        return self.session.get(url).content

    def get_first_view(self, format='json'):
        """
        Get a first view model as dict

        :return:
        """
        url = self.__url + 'views/first'
        return self.session.get(url).json()

    def get_view(self, view_id, format='json'):
        """
        :param view_id:
        :param format:

        :return :
        """
        if format is 'json':
            url = self.__url + 'views/' + str(view_id)
            return self.session.get(url).json()
        elif format is 'view':
            return self.__get_view_object(view_id)
        else:
            return None

    def __get_view_object(self, view_id):
        """
        Create a new CyNetworkView object for the given ID.

        :param view_id:
        :return:
        """
        view = CyNetworkView(self, view_id)
        return view

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__id == other.__id
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


def check_response(res):
    """
    Check HTTP response and raise exception if response is not OK.

    :param res:
    """
    try:
        res.raise_for_status() # ALternative is res.ok
    except Exception as exc:
        # Bad response code, e.g. if adding an edge with nodes that doesn't exist
        try:
            err_info = res.json()
            err_msg = err_info['message'] # or 'localizeMessage'
        except ValueError:
            err_msg = res.text[:40] # Take the first 40 chars of the response
        except KeyError:
            err_msg = res.text[:40] + ("(No 'message' in err_info dict: %s"
                                       % list(err_info.keys()))
        exc.args += (err_msg,)
        raise exc
