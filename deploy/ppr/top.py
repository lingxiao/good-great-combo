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
gr_path     = PATH['assets']['graph']


'''
	@Use: split edges into chunks to compute
	      weight on remote 
'''
def run_split(size, output_dir):

	_, words = load_as_list(gr_path)
	splits   = list(chunks(words,size))

	cnt = 1

	print('\n>> splitting words into ' + str(len(splits)) + ' chunks')
	
	for ws in splits:
		path = os.path.join(output_dir, 'word-' + str(cnt) + '.txt')
		with open(path,'wb') as h:
			for w in ws:
				h.write(w + '\n')
		cnt += 1

	return cnt

'''
	@Use: rewrite main-#.py file
'''
def run_auto_main(tot):

	cnt = 2

	for k in xrange(tot - 2):
		src_path = os.path.join(_script_dir, 'main-1.py')
		tgt_path = os.path.join(_script_dir, 'main-' + str(cnt) + '.py')
		src_str  = 'batch = 1'
		tgt_str  = 'batch = ' + str(cnt)
		auto_gen(src_path, tgt_path, src_str, tgt_str)
		cnt += 1

'''
	@Use: rewrite main-#.sh file
'''
def run_auto_sh(tot):

	cnt = 2

	for k in xrange(tot - 2):
		src_path = os.path.join(_script_dir,'main-1.sh')
		tgt_path = os.path.join(_script_dir,'main-' + str(cnt) + '.sh')
		src_str  = 'main-1'
		tgt_str  = 'main-' + str(cnt)

		auto_gen(src_path, tgt_path, src_str, tgt_str)

		cnt +=1

'''
	run all
'''
n = run_split(10, _word_dir)
# run_auto_main(n)
# run_auto_sh  (n)




