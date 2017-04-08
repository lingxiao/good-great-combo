############################################################
# Module  : base compare and superlative adjectives
# Date    : December 22nd
# Author  : Xiao Ling
# Source  : http://www.enchantedlearning.com/grammar/partsofspeech/adjectives/comparatives.shtml
############################################################

import os
import pickle
from utils import *
from app.config import *
from experiments import *

'''
	conclusion: the values do not make sense
	           either there's a bug or 
	           there's too much noise
'''

############################################################
'''
	experiment output path

'''
exp_out = os.path.join(PATH['experiments']['least-squares'], 'output')

############################################################
'''
	@Use: load graph from `gr_path` 
	      construct A,x,b and save A , b
	      to `out_dir`
'''
def solve_for_adverb(gr_path, out_dir):

	sub_G      = labeled_subgraph(gr_path)

	x,b_lookup = init_labled_adjectives( sub_G['graph']
	                            , sub_G['base']
	                            , sub_G['compare']
	                            , sub_G['superla'])


	A,b = to_Ab(sub_G['graph'], x, b_lookup)

	A_path  = os.path.join(out_dir, 'A-matrix.txt')
	b_path  = os.path.join(out_dir, 'b-vector.txt')

	row_str = lambda r : ','.join([str(x) for x in r])
	A_save  = [row_str(r) for r in A]
	b_save  = '\n'.join(str(x) for x in b)

	with open(A_path, 'wb') as h:
		for a in A_save:
			h.write(a + '\n')

	with open(b_path, 'wb') as h:
		h.write(b_save)		

	return x, b_lookup, os.path.join(out_dir, 'x-vector.txt')

def read_x(path,x_lookup):
	x = [float(x) for x in open(path, 'r').read().split('\n')[0:-1]]
	x = dict(zip(x_lookup,x))
	return x

'''
instructions:
		(1) run solve_for_adverb 
		(2) open learn.m and run it following
			instructions found there
		(3) 
'''
# x, b, x_path = solve_for_adverb(PATH['assets']['graph'], exp_out)
# x_vector = read_x(x_path, x)
    





