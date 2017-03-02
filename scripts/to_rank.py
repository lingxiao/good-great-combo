############################################################
# Module  : rank
# Date    : December 10th
# Author  : Xiao Ling
############################################################

from scripts import *
from prelude import * 


############################################################
'''
  @Use: given milp object, output ranking
        as list of lists

  prob_to_algo_rank :: MILP -> [[String]] -> [[String]]
'''  
def prob_to_algo_rank(prob,words):

  raw = [v.name.split('=') for v in prob.variables() \
        if v.varValue == 1.0]
  raw = [(u.replace('s_',''),v) for [u,v] in raw]
  raw = [(u.replace('_','-'), v.replace('_','-')) for u,v in raw]

  # construct graph :: dictionary for topological sort
  order = dict()        

  for s,w in raw:
    if s in order:
      order[s] += [w]
    else:
      order[s] = [w]

  # complete the sink in the dictonary
  for w in words:
    if w not in order: order[w] = []

  return [[w] for w in toposort(order)]

