############################################################
# Module  : A series of measures on the graph for experiments
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
import re
import networkx as nx

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

'''
	@Use: collect ngram counts
'''
batch = 0

word_path    = os.path.join(_word_dir  , 'word-' + str(batch) + '.txt')
pattern_path = PATH['assets']['patterns']
ngram_dir    = PATH['ngrams']
out_dir      = _output_dir
log_dir      = PATH['directories']['log']

collect_ngram_patterns( word_path
	                  , pattern_path
	                  , ngram_dir
	                  , out_dir
	                  , log_dir)


# patterns  = read_pattern(pattern_path)
# pairs     = [x.split(', ') for x in open(word_path,'rb').read().split('\n') if x]
# results   = {(s,t) : {'weak-strong' : [], 'strong-weak': []} for s,t in pairs}           


# '''
# 	iterate over all ngrams and parse all permutations of s R t
# 	for words s,t and patterns R
# '''
# for gram,n in with_ngram(ngram_dir):

# 	for s,t in pairs:

# 		for R in patterns['strong-weak']:

# 			reg = re.compile(parse_re(R,[s,t]))

# 			if reg.match(gram):
# 				results[(s,t)]['strong-weak'].append((gram,n))

# 		for R in patterns['weak-strong']:

# 			reg = re.compile(parse_re(R,[t,s]))

# 			if reg.match(gram):
# 				results[(s,t)]['strong-weak'].append((gram,n))

# 		for R in patterns['weak-strong']:

# 			reg = re.compile(parse_re(R,[s,t]))
# 			if reg.match(gram):
# 				results[(s,t)]['weak-strong'].append((gram,n))

# 		for R in patterns['strong-weak']:

# 			reg = re.compile(parse_re(R,[t,s]))
# 			if reg.match(gram):
# 				results[(s,t)]['weak-strong'].append((gram,n))


# '''
# 	save outputs for each s-t pairs
# '''
# for (s,t),res in pairs.iteritems():

# 	if res['strong-weak'] or res['weak-strong']:

# 		with open(os.path.join(out_dir, s + t + '.txt'), 'wb') as h:
# 			h.write('=== strong-weak\n')

# 			for p in res['strong-weak']:
# 				h.write(p + '\n')

# 			h.write('=== weak-strong\n')

# 			for q in res['weak-strong\n']:
# 				h.write(q + '\n')

# 			h.write('=== END')















