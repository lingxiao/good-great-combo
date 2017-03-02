############################################################
# Module  : Toplogical Sort
# Date    : December 11th
# Author  : https://algocoding.wordpress.com/2015/04/05/topological-sorting-python/
############################################################

from collections import deque

def toposort(graph):
    xs = go_topsort(graph)
    xs.reverse()
    return xs

def go_topsort(graph):
    in_degree = { u : 0 for u in graph }     # determine in-degree 
    for u in graph:                          # of each node
        for v in graph[u]:
            in_degree[v] += 1
 
    Q = deque()                 # collect nodes with zero in-degree
    for u in in_degree:
        if in_degree[u] == 0:
            Q.appendleft(u)
 
    L = []     # list for order of nodes
     
    while Q:                
        u = Q.pop()          # choose node of zero in-degree
        L.append(u)          # and 'remove' it from graph
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                Q.appendleft(v)
 
    if len(L) == len(graph):
        return L
    else:                    # if there is a cycle,  
        raise NameError('graph has cycle')
        # print('================ graph has cycle =============')
        return []


