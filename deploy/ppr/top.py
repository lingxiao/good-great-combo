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
_word_dir   = os.path.join(_root , 'words') 
_output_dir = os.path.join(_root , 'outputs')
_script_dir = os.path.join(_root ,'scripts')
_shell_dir  = os.path.join(_root ,'shell')
gr_path     = PATH['assets']['graph']


############################################################
'''
	@Use: rewrite main-#.py file
'''
def run_auto_main(alphas):

	for k in alphas:
		src_path = os.path.join(_root, 'main-0.py')
		tgt_path = os.path.join(_script_dir, 'main-' + str(k) + '.py')
		src_str  = 'alpha = 0'
		tgt_str  = 'alpha = ' + str(k)
		auto_gen(src_path, tgt_path, src_str, tgt_str)

'''
	@Use: rewrite main-#.sh file
'''
def run_auto_sh(alphas):

	for k in alphas:
		src_path = os.path.join(_root,'main-0.sh')
		tgt_path = os.path.join(_shell_dir,'main-' + str(k) + '.sh')
		src_str  = 'main-0'
		tgt_str  = 'main-' + str(k)

		auto_gen(src_path, tgt_path, src_str, tgt_str)



############################################################
'''
	run all
'''
alphas = [0.9,0.8,0.7,0.5,0.25,0.1,0.01]

run_auto_main(alphas)
run_auto_sh  (alphas)




