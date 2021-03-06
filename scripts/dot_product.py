############################################################
# Module  : compute dot product between two word vectors
# Date    : December 22nd
# Author  : Xiao Ling
# Source  : http://www.enchantedlearning.com/grammar/partsofspeech/adjectives/comparatives.shtml
############################################################

import os
import numpy as np
from utils import *


'''
	@Use: compute word2vec values for all words and save
	@Input: `word_2_vec_path` :: String, path to word2vec .txt file
			`word_pair_path`  :: String, path to .txt with word pairs in form:
											word1, word2
			`output_dir`      :: String, path to save results										
			`refresh`         :: Bool, if true do not recompute value

	@Returns: None			
'''
def dot(word_2_vec_path, word_pair_path, out_dir, refresh):

	print('\n>> running `dot` with refresh = ' + str(refresh))

	vector,ws = read_vector(word_2_vec_path)

	pairs     = [x.split(', ') for x in open(word_pair_path,'rb').read().split('\n') \
	            if len(x.split(', ')) == 2]

	print('\n>> found ' + str(len(pairs)) + ' total pairs that need to be computed')

	if refresh: 
		# exists = [to_path(s,t,out_dir) for s,t in pairs]          
		pairs  = [(s,t) for (s,t) in pairs \
		          if not os.path.exists(to_path(s,t,out_dir))]

	print('\n>> found ' + str(len(pairs)) + ' pairs that need to be computed still')	          

	for s,t in pairs:
		v = np.dot(vector[s], vector[t])
		with open(to_path(s,t,out_dir),'wb') as h:
			h.write(str(v))


def to_path(s,t,out_dir):
	return os.path.join(out_dir, s +'-' + t + '.txt')


def read_vector(word_2_vec_path):

	vector = dict()
	words  = []

	with open(word_2_vec_path,'rb') as vec:
		for v in vec:
			if v:
				v = v.split(' ')
				word = v[0]
				v    = [float(x) for x in v[1:-1]]

				if word != '\n':
					vector[word] = np.asarray(v)
					words.append(word)

	return vector, words



