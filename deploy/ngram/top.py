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
_root       = os.path.join(PATH['directories']['deploy'], 'ngram')
_word_dir   = os.path.join(_root, 'word-pairs') 
_output_dir = os.path.join(_root, 'outputs')
_script_dir = os.path.join(_root ,'scripts')
_shell_dir  = os.path.join(_root ,'shells' )
gr_path     = PATH['assets']['graph']
ccb         = read_gold(PATH['assets']['ccb'])
bansal      = read_gold(PATH['assets']['bansal'])


'''
	construct unique pairs of words 
'''
def to_unique_pairs(words):
	tup   = lambda xs : (xs[0], xs[1])
	pairs = set(tup(sorted([u,v])) for u in words for v in words if u != v)
	return list(pairs)

'''
	@Use: split edges into chunks to compute
	      weight on remote 
'''
def run_split(size, output_dir):

	'''
		get all words
	'''
	bansal_words = join(join(ws) for _,ws in bansal.iteritems())
	ccb_words    = join(join(ws) for _,ws in bansal.iteritems())

	_, words = load_as_list(gr_path)

	'''
		construct word pairs
	'''
	words    = words + bansal_words + ccb_words
	pwords   = to_unique_pairs(words)
	splits   = list(chunks(pwords,size))

	cnt = 1

	print('\n>> splitting words pairs into ' + str(len(splits)) + ' chunks')
	
	for ws in splits:

		path = os.path.join(output_dir, 'word-' + str(cnt) + '.txt')

		with open(path,'wb') as h:
			for s,t in ws:
				h.write(s + ', ' + t + '\n')

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
		src_path = os.path.join(_shell_dir,'main-1.sh')
		tgt_path = os.path.join(_shell_dir,'main-' + str(cnt) + '.sh')
		src_str  = 'main-1'
		tgt_str  = 'main-' + str(cnt)

		auto_gen(src_path, tgt_path, src_str, tgt_str)

		cnt +=1

'''
	run all
'''
n = run_split(50000, _word_dir)
run_auto_main(n)
run_auto_sh  (n)

