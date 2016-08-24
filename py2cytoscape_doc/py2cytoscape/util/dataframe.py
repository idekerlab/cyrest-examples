# -*- coding: utf-8 -*-
"""
Data conversion utilities for dataframe
=====================================

Convert cytoscape.js style graphs from/to dataframe object.


"""

import pandas as pd
from . import cytoscapejs as cyjs


def from_dataframe(df, source_col='source', target_col='target', interaction_col='interaction',
                   name='From DataFrame', edge_attr_cols=[]):
    """
    Utility to convert Pandas DataFrame object into Cytoscape.js JSON

    :param df: the data frame object.
    :param source_col: the column name of source column.
    :param target_col: the column name of target column.
    :param interaction_col: the column name of interaction column.
    :param name: The network name.
    :param edge_attr_cols: Now, this parapeter is not valid.

    :return: the Cytoscape.js JSON
    """
    network = cyjs.get_empty_network(name=name)
    nodes = set()

    for index, row in df.iterrows():
        s = row[source_col]
        t = row[target_col]
        if s not in nodes:
            nodes.add(s)
            source = get_node(s)
            network['elements']['nodes'].append(source)
        if t not in nodes:
            nodes.add(t)
            target = get_node(t)
            network['elements']['nodes'].append(target)

        network['elements']['edges'].append(get_edge(s, t, interaction=row[interaction_col]))
    return network


def to_dataframe(network, interaction='interaction', default_interaction='-'):
    """
    This method convert Cytoscape.js JSON to Pandas DataFrame.

    :param network: The Cytoscape.js JSON
    :param interaction: The column name of interaction
    :param default_interaction: The defalt value of interaction.

    :return : The Pandas DataFrame object.
    """
    edges = network['elements']['edges']

    network_array = []
    for edge in edges:
        edge_data = edge['data']
        source = edge_data['source']
        target = edge_data['target']
        if interaction in edge_data:
            itr = edge_data[interaction]
        else:
            itr = default_interaction
        row = (source, itr, target)
        network_array.append(row)

    return pd.DataFrame(network_array, columns=['source', 'interaction',
                                                'target'])


def get_node(id):
    """
    Get the node information in JSON format.

    :param id: The network node id or name.

    :return : the json object about node.
    """
    node = {
        'data': {
            'id': str(id),
            'name': str(id)
        }
    }
    return node


def get_edge(source, target, interaction):
    """
    Get the edge information in JSON format.

    :param source: the id or name of source node.
    :param target: the id or name of target node.
    :param interaction: the interaction of edge.

    :return : the JSON value about edge.
    """
    if interaction is None:
        itr = '-'
    else:
        itr = interaction

    edge = {
        'data': {
            'source': source,
            'target': target,
            'interaction': itr
        }
    }

    return edge
