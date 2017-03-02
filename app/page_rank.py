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
from random import *

from prelude import *

############################################################
'''
	build adjacency nbit vector

	given ordered list of adjectives, 
	output nbit list where ith element = 1
	if ith word appear in words
'''
def encode(adjectives, words):
	edges = []
	for a in adjectives:
		count = len([x for x in words if x == a])
		if a in words: edges.append(count)
		else         : edges.append(count)
	return edges

'''
	given ordered list of adjectives, 
	and nbit list where ith element = 1
	output corresponding word list
'''
def decode(adjectives, n_bit):
	return [w for w,b in zip(adjectives,n_bit) if b]

'''
	given full graph and list of edges (adverbs)
	to include, build adjacency matrix

	Note: the rows of this matrix correspondes
	to vectors of a conventional adjacency matrix
	you need to transpose the matrix in matlab before
	using it under the 'intuitive' manner
'''
def to_adjacency_matrix(graph, adverbs):

	adjectives = set(join([[u,v] for u,v,_ in graph]))
	matrix     = []

	for a in adjectives:
		'''
			outgoing edges from adjective a
		'''
		words = [v for u,v,z in graph if u == a and z in adverbs]
		e_a   = encode(adjectives,words)
		matrix.append(e_a)

	return matrix

############################################################
'''
	save adjacency matrix and open
'''	

def save_adjency_matrix(root, name, matrix):

	p = os.path.join(root, name + '.txt')
	h = open(p,'w')

	for v in matrix:
		w = ','.join(str(x) for x in v)
		h.write(w + '\n')
	h.close()	

	return p


def open_adjacency_matrix(root,name):

	h   = open(os.path.join(root,name + '.txt'),'r').read().split('\n')
	mat = [v.split(',') for v in h if v]
	mat = [[int(b) for b in v] for v in mat]
	return mat


############################################################
'''
	run program

	PATHS
'''
root     = "/Users/lingxiao/Documents/research/code/good-great-ppdb"
gold_ccb = os.path.join(root, 'inputs/testset-ccb.txt' )
gold_moh = '/Users/lingxiao/Documents/research/code/good-great-ngrams/inputs/testset-bansal.txt'
graph_p  = os.path.join(root, 'inputs/raw/all_edges.txt'  )
output   = os.path.join(root, 'outputs')

'''
	open Veronica's raw graph
'''
graph_r = label_adv(split_comma(open(graph_p,'r' ).read().split('\n')))
graph_r = [(u,v,w) for u,v,w in graph_r if u != v]

# graph = graph_r
graph   = graph_r[100:200] + graph_r[1000:1100]

'''
	build and save graph
'''
# adverbs = ['<very>']
adverbs = set(v for _,_,v in graph)
matrix  = to_adjacency_matrix(graph,adverbs)
name    = 'adjacency-all-adverbs'
path    = save_adjency_matrix(output, name, matrix)	




























