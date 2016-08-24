# -*- coding: utf-8 -*-
"""
This is the utility for cytoscape.js obejct.
=====================================


"""
import copy

EMPTY_NETWORK = {
    'data': {
    },

    'elements': {
        'nodes': [],
        'edges': []
    }
}


def get_empty_network(name='Empty Network'):
    """
    Get empty network in the cytoscape.js style.

    :param name: the empty network's name.

    :return : the empty network's cytoscape.js style object.
    """
    empty_network = copy.deepcopy(EMPTY_NETWORK)
    empty_network['data']['name'] = name
    return empty_network
