############################################################
# Module  : base compare and superlative adjectives
# Date    : December 22nd
# Author  : Xiao Ling
# Source  : http://www.enchantedlearning.com/grammar/partsofspeech/adjectives/comparatives.shtml
############################################################

import os
from nltk.stem.wordnet import WordNetLemmatizer

from utils import *
from app.config import *

############################################################
'''
    Load assets from paths
'''
# G :: [(String,String,String)]
# w :: [String]
G,words = load_as_list(PATH['assets']['graph'])

# A0,b0,x_lookup0 = to_Ab(subgraph0,b_lookup0)

############################################################
'''
    @Use: construct subgraph with all base, comparatives, and superlative forms
    @Input : `graph_path` :: String path to graph 
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
def labeled_subgraph(graph_path):

    G,_ = load_as_list(graph_path)

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

    ############################################################
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

sub_G = labeled_subgraph(PATH['assets']['graph'])

############################################################
'''
    @Use: Given subgraph of base, compariatve and superlative
          adjectives and, and the list of wordss
          output the adjectives with preset values
    @Input: subgraph :: [(String, String, String)]
            base     :: [String]
            compare  :: [String]
            superla  :: [String]
    @Output: x_lookup :: Dict String Float
             b_lookup :: [String]
'''
def init_labled_adjectives(subgraph, base, compare, superla):

    stride      = 1/3.0
    base_val    = 1/3.0
    compare_val = base_val + stride
    superla_val = compare_val + stride

    # set of adjectives whose value is arbitrariliy assigned
    b_lookup = dict([(w, base_val)    for w in base]    \
                  + [(w, compare_val) for w in compare] \
                  + [(w, superla_val) for w in superla])

    # set of adverbs whose value to be solved
    x_lookup = list(set(v for _,_,v in subgraph))

    return x_lookup, b_lookup

'''
    @Use: Construct A x = b give subgraph
    @Input: - `subgraph`:: [(String,String,String)]
            - x_lookup  :: Dict String Float
            - b_lookup  :: [String]

    @Output: A matrix, b vector, 
             also saved to common space shared with matlab
'''
def to_Ab(subgraph, x_lookup, b_lookup):

    A = []
    b = [0]*len(subgraph)

    for s,t,v in subgraph:
        row       = [0]*len(x_lookup)
        r         = subgraph.index((s,t,v))

        # s + v = t  ==> s + v - t = s + v - t
        if s in b_lookup and t in b_lookup and v in b_lookup:
            b[r] = b_lookup[s] + b_lookup[v] - b_lookup[t]
            row[x_lookup.index(s)] = 1.0
            row[x_lookup.index(v) ] = 1.0
            row[x_lookup.index(t)] = -1.0

        # s + v = t  /\ not v ==> v = t - s
        elif s in b_lookup and t in b_lookup and v not in b_lookup:
            b[r] = b_lookup[t] - b_lookup[s]
            row[x_lookup.index(v)] = 1

        # s + v = t /\ not t ==> t = s + v
        elif s in b_lookup and t not in b_lookup and v in b_lookup:
            b[r] = b_lookup[s] + b_lookup[v]
            row[x_lookup.index(t)]  = 1

        # s + v = t /\ not s ==> s = t - v
        elif s not in b_lookup and t in b_lookup and v in b_lookup:
            b[r] = b_lookup[t] - b_lookup[v]
            row[x_lookup.index(s)] = 1

        # s + v = t /\ not t /\ not v ==> t - v = s
        elif s in b_lookup and t not in b_lookup and v not in b_lookup:
            b[r] = b_lookup[s]
            row[x_lookup.index(t)] = 1
            row[x_lookup.index(v)]  = -1

        # s + v = t /\ not s /\ not v ==> s + v = t
        elif s not in b_lookup and t in b_lookup and v not in b_lookup:
            b[r] = b_lookup[t]
            row[x_lookup.index(s)] = 1
            row[x_lookup.index(v) ] = 1

        # s + v = t /\ not s /\ not t ==> t - s = v
        elif s not in b_lookup and t not in b_lookup and v in b_lookup:
            b[r] = b_lookup[v]
            row[x_lookup.index(s)] = -1
            row[x_lookup.index(t)] =  1

        # s + v = t /\ not s /\ not t /\ not s ==> s + v - t = 0
        elif s not in b_lookup and t not in b_lookup and v not in b_lookup:
            row[x_lookup.index(s)] = 1
            row[x_lookup.index(v) ] = 1
            row[x_lookup.index(t)] = -1
        else:
            raise NameError("unaccounted case") 

        A.append(row)

    return A, b


'''
    Given A and b matrix, save to   
        path/A_name.txt
        path/b_name.txt
'''
def save_Ab(A,b, path, A_name, b_name):
    '''
        Save as text file for matlab solver
    '''
    row_str = lambda r : ','.join([str(x) for x in r])
    A_path  = os.path.join(path, A_name + '.txt')
    f       = open(A_path,'w')
    A_save  = [row_str(r) for r in A]

    save_list(f,A_save)
    f.close()

    b_path = os.path.join(path, b_name + '.txt')
    h      = open(b_path,'w')
    bstr   = '\n'.join(str(x) for x in b)
    h.write(bstr)
    h.close()

    return (A_path, b_path)

x,b_lookup = init_labled_adjectives( sub_G['graph']
                            , sub_G['base']
                            , sub_G['compare']
                            , sub_G['superla'])



A,b = to_Ab(sub_G['graph'], x, b_lookup)

# save_Ab(A,b, pdir, 'A-matrix','b-vector')



    




