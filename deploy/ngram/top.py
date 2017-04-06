############################################################
# Module  : get google ngram lines that contain words in graph
#           split edges and make main-#.py
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
_pair_dir   = os.path.join(_root, 'word-pairs') 
_word_dir   = os.path.join(_root, 'words')
_output_dir = os.path.join(_root, 'outputs')
_script_dir = os.path.join(_root ,'scripts')
_shell_dir  = os.path.join(_root ,'shells' )
gr_path     = PATH['assets']['graph']
ccb         = read_gold(PATH['assets']['ccb'])
bansal      = read_gold(PATH['assets']['bansal'])

############################################################


'''
	@Use: combine batched ngrams into one file
	      and remove duplicates
	@Input: input directory `input_dir`    :: String
	        output file path `output_path` :: String

	@Output: None. write output to disk at `output_path`
'''
def concat_ngrams(input_dir, output_path):

	paths = [os.path.join(input_dir, p) for p in os.listdir(input_dir) if '.txt' in p]

	ngrams = []

	for p in paths:
		print('\n>> concatting ngrams from ' + p)
		xs = [ x.split(': ') for x in open(p,'rb').read().split('\n')]
		ngrams += [(x[0],x[1]) for x in xs if len(x) == 2]

	ngrams = set(ngrams)

	print ('\n>> saving at ' + output_path)
	with open(output_path,'wb') as h:
		for xs,n in ngrams:
			h.write(xs + '\t' + n + '\n')

############################################################
'''
	@Use: split all words in graph
'''
def split_into_words(size, output_dir):

	'''
		get all words
	'''
	bansal_words = join(join(ws) for _,ws in bansal.iteritems())
	ccb_words    = join(join(ws) for _,ws in bansal.iteritems())

	_, words = load_as_list(gr_path)

	'''
		construct word pairs
	'''
	words    = list(set(words + bansal_words + ccb_words))
	splits   = list(chunks(words, size))

	print(len(words))

	cnt = 1

	print('\n>> splitting words into ' + str(len(splits)) + ' chunks')
	
	for ws in splits:

		path = os.path.join(output_dir, 'batch-' + str(cnt) + '.txt')

		with open(path,'wb') as h:
			for w in ws:
				h.write(w + '\n')

		cnt += 1

	return cnt

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
def split_into_pairs(size, output_dir):

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

		path = os.path.join(output_dir, 'batch-' + str(cnt) + '.txt')

		with open(path,'wb') as h:
			for s,t in ws:
				h.write(s + ', ' + t + '\n')

		cnt += 1

	return cnt

############################################################
'''
	@Use: rewrite main-#.py file
'''
def run_auto_main(tot):

	cnt = 1

	for k in xrange(tot):
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

	cnt = 1

	for k in xrange(tot):
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
# n = split_into_words(250, _word_dir)
n = split_into_pairs(200000, _pair_dir)
run_auto_main(n)
run_auto_sh  (n)

# concat_ngrams('/nlp/users/xiao/good-great-combo/ngrams/word-ngrams', '/nlp/users/xiao/good-great-combo/ngrams/full/word-ngrams.txt')
# concat_ngrams(_output_dir, os.path.join(_output_dir, 'ngram-words.txt'))



