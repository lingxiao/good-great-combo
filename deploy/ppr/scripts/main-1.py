############################################################
# Module  : A series of measures on the graph for experiments
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os

from utils   import *
from scripts import *
from app.config import PATH

import networkx as nx

############################################################
'''
	paths
'''
_root       = os.path.join(PATH['directories']['deploy'], 'ppr')
_word_dir   = os.path.join(_root, 'words') 
_output_dir = os.path.join(_root, 'outputs')
_script_dir = os.path.join(_root ,'scripts')
gr_path     = PATH['assets']['graph']


'''
	@Use: compute ppr for each word
'''
batch = 1

in_path  = os.path.join(_word_dir  , 'word-' + str(batch) + '.txt')
out_path = os.path.join(_output_dir, 'word-' + str(batch) + '.txt')



