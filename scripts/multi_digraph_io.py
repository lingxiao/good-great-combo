############################################################
# Module  : Naive implementation
# Date    : Feburary 13th 2017
# Author  : Xiao Ling, merle
############################################################

import os
import json
from networkx.readwrite import json_graph

def digraph_from_json(path):
    with open(path, 'r') as infile:
        networkx_graph = json_graph.node_link_graph(json.load(infile))
    return networkx_graph

def digraph_to_json(networkx_graph):
    return json.dumps(json_graph.node_link_data(self.nx_graph))