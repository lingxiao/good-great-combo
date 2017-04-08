############################################################
# Module  : compute edge weight where 
# 
#           			   | s -> t | 
# w(s -> t) =          ---------------------------
#                      	 | s -> t |  + | t -> s |
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
_root       = os.path.join(PATH['directories']['deploy'], 'edge-wt-bradley-terry')
_edge_dir   = os.path.join(_root, 'edges'  )
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

'''
	@Use: split edges into chunks to compute
	      weight on remote 
'''
def split_bradley_terry(size):

	edges, words = load_as_list(gr_path)

	to_tuple     = lambda xs: (xs[0], xs[1])
	unique_edges = list(set( to_tuple(sorted([u,v])) for u in words for v in words ))

	print('\n>> there are ' + str(len(unique_edges)) + ' total possible edges in graph')

	splits       = list(chunks(unique_edges,size))

	splits = [[('good','great'), ('good', 'excellent'),('good','bad')]] + splits

	print('\n>> splitting into ' + str(len(splits)) + ' set of edges of ' 
		  + ' of length ' + str(len(splits[2])) + ' each')

	cnt = 0
	
	for xs in splits:
		path = os.path.join(_edge_dir, 'edge-' + str(cnt) + '.txt')
		with open(path,'wb') as h:
			for s,t in xs:
				h.write(s + ', ' + t + '\n')
		cnt += 1

	return cnt

############################################################
'''
	run all
'''
n = split_bradley_terry(100000)
run_auto_main(n)
run_auto_sh  (n)




