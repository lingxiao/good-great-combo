############################################################
# Module  : base compare and superlative adjectives
# Date    : December 22nd
# Author  : Xiao Ling
# Source  : http://www.enchantedlearning.com/grammar/partsofspeech/adjectives/comparatives.shtml
############################################################

import os

from utils import *
from app.config import *
from experiments import *

############################################################
'''
    Load assets from paths
'''
sub_G      = labeled_subgraph(PATH['assets']['graph'])

x,b_lookup = init_labled_adjectives( sub_G['graph']
                            , sub_G['base']
                            , sub_G['compare']
                            , sub_G['superla'])



A,b = to_Ab(sub_G['graph'], x, b_lookup)

# save_Ab(A,b, pdir, 'A-matrix','b-vector')



    





