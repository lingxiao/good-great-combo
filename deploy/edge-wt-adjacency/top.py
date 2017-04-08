############################################################
# Module  : compute edge weight where 
# 
#           			   | s -> t | 
# w(s -> t) =          -------------------
#                      	 sum_x  | s -> x|
# 
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
from utils   import *
from scripts import *
from app.config import PATH

############################################################
'''
	paths
'''
_root       = os.path.join(PATH['directories']['deploy'], 'edge-wt-adjacency')
_edge_dir   = os.path.join(_root, 'edges')
_output_dir = os.path.join(_root, 'outputs')
_script_dir = os.path.join(_root ,'scripts')
_shell_dir  = os.path.join(_root ,'shells' )

gr_path     = PATH['assets']['graph']

############################################################
'''
	@Use: rewrite main-#.py file
'''
def run_auto_main(tot):

	cnt = 0

	for k in xrange(tot-1):
		src_path = os.path.join(_root, 'main-0.py')
		tgt_path = os.path.join(_script_dir, 'main-' + str(cnt) + '.py')
		src_str  = 'batch = 0'
		tgt_str  = 'batch = ' + str(cnt)
		auto_gen(src_path, tgt_path, src_str, tgt_str)
		cnt += 1

'''
	@Use: rewrite main-#.sh file
'''
def run_auto_sh(tot):

	cnt = 0

	for k in xrange(tot-1):
		src_path = os.path.join(_root,'main-0.sh')
		tgt_path = os.path.join(_shell_dir,'main-' + str(cnt) + '.sh')
		src_str  = 'main-0'
		tgt_str  = 'main-' + str(cnt)

		auto_gen(src_path, tgt_path, src_str, tgt_str)

		cnt +=1

############################################################
'''
	run all
'''
edge_paths = [os.path.join(_edge_dir,p) for p in os.listdir(_edge_dir)]

n = len(edge_paths)
run_auto_main(n)
run_auto_sh  (n)



