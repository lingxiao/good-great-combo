############################################################
# Module  : pick out subgraph with base comparative and
#           superlative pairs
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

from scripts import *
from utils import *

'''
    @Use: construct subgraph with all base, comparatives, and superlative forms
    @Input : `G` :: [(String, String,String)]
    @Output: dict with keys:
        - "graph"  :: [(String,String,String)]
            subgraph where each (s,t,v) triple indicates:
            an edge from s to t with adverb v
            for the paraphrase:
                v s = t
            where each s and t are either base, superlative
            or compariatve adjectives

       - "base"    :: [String] list of base words
       - "compare" :: [String] list of compariatve words
       - "superla" :: [String] list of superlative words

'''
def training_graph(G):


    G_base_compare    = [(s,t,v) for s,t,v in G if base_compare(s,t)   ]
    G_compare_base    = [(s,t,v) for s,t,v in G if compare_base(s,t)   ]
    G_base_superla    = [(s,t,v) for s,t,v in G if base_superla(s,t)   ]
    G_superla_base    = [(s,t,v) for s,t,v in G if superla_base(s,t)   ]
    G_compare_superla = [(s,t,v) for s,t,v in G if compare_superla(s,t)]
    G_superla_compare = [(s,t,v) for s,t,v in G if superla_compare(s,t)]

    subgraph = G_base_compare        \
             + G_compare_superla     \
             + G_base_superla        \
             + G_superla_base        \
             + G_compare_superla     \
             + G_superla_compare

    '''
        get all base compare and superla forms from graph
    '''
    base = set([s for s,_,_ in G_base_compare] \
             + [t for _,t,_ in G_compare_base] \
             + [s for s,_,_ in G_base_superla] \
             + [t for _,t,_ in G_superla_base])

    compare = set([x for _,x,_ in G_base_compare] \
                 + [x for x,_,_ in G_compare_base] \
                 + [x for x,_,_ in G_compare_superla] \
                 + [x for _,x,_ in G_superla_compare])

    superla = set([x for _,x,_ in G_base_superla] \
                 + [x for x,_,_ in G_superla_base] \
                 + [x for _,x,_ in G_compare_superla] \
                 + [x for x,_,_ in G_superla_compare])

    return { 'graph'   : subgraph
           , 'base'    : list(base)
           , 'compare' : list(compare)
           , 'superla' : list(superla)}





           