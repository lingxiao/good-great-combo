############################################################
# Module  : A series of measures on the graph for experiments
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
import numpy as np

from utils   import *
from scripts import *
from app.config import PATH

############################################################
'''
	paths
'''
batch = 65

_root          = os.path.join(PATH['directories']['deploy'], 'dot-product')
_pair_dir      = os.path.join(_root, 'pairs')
_output_dir    = os.path.join(_root, 'outputs')

word_2_vec_big = PATH['inputs']['word2vec']
word_2_vec_sm  = PATH['inputs']['word2vec-sm']

word_pair_path = os.path.join(_pair_dir  , 'batch-' + str(batch) + '.txt')
out_path       = os.path.join(_output_dir, 'batch-' + str(batch) + '.txt')

dot(word_2_vec_big, word_pair_path, _output_dir, refresh = True)


















