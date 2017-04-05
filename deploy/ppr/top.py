############################################################
# Module  : split edges and make main-#.py
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
import json
import networkx as nx

import re

from utils   import *
from scripts import *
from app.config import PATH

############################################################
'''
	paths
'''
_root       = os.path.join(PATH['directories']['deploy'], 'ppr')
_word_dir   = os.path.join(_root, 'words') 
_output_dir = os.path.join(_root, 'outputs')
_script_dir = os.path.join(_root ,'scripts')
_shell_dir = os.path.join(_root ,'shell')
gr_path     = PATH['assets']['graph']


'''
	@Use: rewrite main-#.sh file
'''
def run_auto_sh(tot):

	cnt = 1

	for k in xrange(tot):
		src_path = os.path.join(_shell_dir,'ppr-0.sh')
		tgt_path = os.path.join(_shell_dir,'ppr-' + str(cnt) + '.sh')
		src_str  = 'ppr-0'
		tgt_str  = 'ppr-' + str(cnt) 

		auto_gen(src_path, tgt_path, src_str, tgt_str)

		cnt +=1

'''
	run all
'''
run_auto_sh  (7)




