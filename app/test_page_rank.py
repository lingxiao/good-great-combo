############################################################
# Module  : Page-rank
# Date    : January 28th, 2017
# Author  : Xiao Ling, merle
############################################################

import os
import datetime
import unittest
from copy import deepcopy
import numpy as np
from prelude import *

def t_encode_decode():

	adjectives = ['good','great','excellent']
	words0     = []
	words1     = ['good']
	words2     = ['great']
	words3     = ['excellent']
	words4     = words1 + words2
	words5     = words1 + words2 + words3

	nbit0      = [0,0,0]
	nbit1      = [1,0,0]
	nbit2      = [0,1,0]
	nbit3      = [0,0,1]
	nbit4      = [1,1,0]
	nbit5      = [1,1,1]


	assert encode(adjectives, words0) == nbit0
	assert encode(adjectives, words1) == nbit1
	assert encode(adjectives, words2) == nbit2
	assert encode(adjectives, words3) == nbit3
	assert encode(adjectives, words4) == nbit4
	assert encode(adjectives, words5) == nbit5


	assert decode(adjectives, nbit0) == words0
	assert decode(adjectives, nbit1) == words1
	assert decode(adjectives, nbit2) == words2
	assert decode(adjectives, nbit3) == words3
	assert decode(adjectives, nbit4) == words4
	assert decode(adjectives, nbit5) == words5

	'''	
		roundtrip
	'''	
	assert encode(adjectives, decode(adjectives, nbit0)) == nbit0
	assert encode(adjectives, decode(adjectives, nbit1)) == nbit1
	assert encode(adjectives, decode(adjectives, nbit2)) == nbit2
	assert encode(adjectives, decode(adjectives, nbit3)) == nbit3
	assert encode(adjectives, decode(adjectives, nbit4)) == nbit4
	assert encode(adjectives, decode(adjectives, nbit5)) == nbit5


	assert decode(adjectives, encode(adjectives, words0)) == words0
	assert decode(adjectives, encode(adjectives, words1)) == words1
	assert decode(adjectives, encode(adjectives, words2)) == words2
	assert decode(adjectives, encode(adjectives, words3)) == words3
	assert decode(adjectives, encode(adjectives, words4)) == words4
	assert decode(adjectives, encode(adjectives, words5)) == words5

	print "passed encode-decode adjacency matrix roundtrip"

def t_adjacency_matrix_roundtrip():

	root     = "/Users/lingxiao/Documents/research/code/good-great-ppdb"

	rand_nbit = lambda n: [randint(0,1) for b in range(1,n+1)]

	rand_mat = [rand_nbit(10) for _ in range(10)]
	name     = 'test-matrix'

	save_adjency_matrix(root, name, rand_mat)

	rand_mat1 = open_adjacency_matrix(root,name)
	 
	assert rand_mat == rand_mat1
	print "passed save-open adjacency matrix roundtrip"

	'''
		tear down
	'''	
	p = os.path.join(root, name + '.txt')
	os.remove(p)


































