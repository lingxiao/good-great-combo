############################################################
# Module  : Scripts to set up Ax = b
# Date    : December 22nd
# Author  : Xiao Ling
############################################################

import os
import re
import datetime
import itertools
import numpy as np

from nltk import pos_tag
from copy import deepcopy

import numpy as np

from scripts import * 
from prelude import *


############################################################
'''
	Generic scripts
'''

'''
	Given x and b vector, and edges, make A matrix
'''
def make_A(x_vector, b_vector, edges):
	A_matrix = []

	for a,b,v in edges:
		row = [0]*len(x_vector)
		row[x_vector.index(a)] = 1
		row[x_vector.index(b)] = -1
		A_matrix.append(row)

	return A_matrix

'''
	Given A and b matrix, save to 	
		root/outputs/A_name.txt
		root/outputs/b_name.txt
'''
def save_Ab(A,b, root, A_name, b_name):
	'''
		Save as text file for matlab solver
	'''
	row_str = lambda r : ','.join([str(x) for x in r])
	A_path  = os.path.join(root,'outputs/' + A_name + '.txt')
	f       = open(A_path,'w')
	A_save  = [row_str(r) for r in A]

	save_list(f,A_save)
	f.close()

	b_path = os.path.join(root,'outputs/' + b_name + '.txt')
	h      = open(b_path,'w')
	bstr   = '\n'.join(str(x) for x in b)
	h.write(bstr)
	h.close()

	return (A_path, b_path)

############################################################
# Learning scripts


'''
	@Use: prep training data for matlab solver
	      write A matrix and b vector to disk

'''
def make_Ab_train(root, env, save):

	data  = env['data']

	fixed = env['fixed']

	'''
		x variable vector = [adjectives, adverbs]
	'''
	x = [a for a in env['adjs'] if a not in fixed] \
	  +  env['advs']

	'''
		b vector
	'''
	b = [0]*len(data)

	'''
		A matrix
	'''
	A = []

	for a1,a2,v in data:

		row = [0]*len(x)
		r   = data.index((a1,a2,v))

		row[x.index(v)] = 1

		if a1 not in x and a2 not in x:
			b[r] = fixed[a2] - fixed[a1]

		else:	
			if a1 in x: row[x.index(a1)] = 1
			else      : b[r] = fixed[a1]

			if a2 in x: row[x.index(a2)] = -1
			else      : b[r] = fixed[a2]


		A.append(row)	

	if save:

		'''
			Save as text file for matlab solver
		'''
		row_str = lambda r : ','.join([str(x) for x in r])
		A_path  = os.path.join(root,'outputs/A-matrix.txt')
		f       = open(A_path,'w')
		A_save  = [row_str(r) for r in A]

		save_list(f,A_save)
		f.close()

		b_path = os.path.join(root,'outputs/b-vector.txt')
		h      = open(b_path,'w')
		bstr   = '\n'.join(str(x) for x in b)
		h.write(bstr)
		h.close()

	return (A,b,x)

'''
	After running prep_Ab and running learn.m
	read the solution to x from dis
'''
def read_solution(root, env, x_lookup):

	'''
		Read in matlab solution
	'''
	fixed = env['fixed']
	x_sol = open(os.path.join(root,'outputs/x-vector.txt'),'r').read().split('\n')
	x_sol = zip (x_lookup, [float(n) for n in x_sol[0:-1]])

	adverbs    = dict((v,n) for v,n in x_sol if v in     env['advs'])
	adjectives = dict((v,n) for v,n in x_sol if v not in env['advs'])

	# combine solved value with values we fixed a-priori
	words      = dict(fixed.items() + dict(x_sol).items())

	return {'x'         : dict(x_sol)
	       ,'adverbs'   : adverbs
	       ,'adjectives': adjectives
	       ,'all'       : words}

############################################################
# Testing Scripts

'''
	@Use: Prep to run solution on test_data
	      by constructing A,b,x
'''
def prep_Ab_test(root, solution, test_data, save):

	x_sol    = solution['x']
	adj_adv  = solution['all']

	'''
		x = vector of unknown adjectives
	'''
	x_t = list(set([a for a,_,_ in test_data if a not in adj_adv] \
		         + [a for _,a,_ in test_data if a not in adj_adv]))


	'''
		b = [  a_fixed  adverbs  ]
	'''
	b_t = [0]*len(test_data)

	'''
		A matrix so that A x = b
	'''
	A_t  = []

	for a1,a2,v in test_data:
		
		r       = test_data.index((a1,a2,v))
		row     = [0]*len(x_t)

		a1_val  = 0
		a2_val  = 0

		if a1 not in adj_adv: 
			row[x_t.index(a1)] = 1.0
		else:
			a1_val = adj_adv[a1]

		if a2 not in adj_adv: 
			row[x_t.index(a2)] = -1.0
		else:
			a2_val = adj_adv[a2]

		A_t.append(row)
		b_t[r]  = adj_adv[v] - a1_val + a2_val

	if save:
		'''
			Save as text file for matlab solver
		'''
		row_str = lambda r : ','.join([str(x) for x in r])
		A_path  = os.path.join(root,'outputs/A-matrix-test.txt')
		f       = open(A_path,'w')
		A_save  = [row_str(r) for r in A_t]

		save_list(f,A_save)
		f.close()

		b_path = os.path.join(root,'outputs/b-vector-test.txt')
		h      = open(b_path,'w')
		bstr   = '\n'.join(str(x) for x in b_t)
		h.write(bstr)
		h.close()

	return (A_t,b_t,x_t)


def mark_label(t):
	[a1_larger, a2_larger, tied, a1,a2] = t
	if a1_larger > a2_larger and a1_larger > tied:
		return (a1, '>', a2)
	elif a2_larger > a1_larger and a2_larger > tied:
		return (a1, '<', a2)
	else:
		return (a1, '==', a2)

'''
	find all adjective1, adjective2, adverb triples
	where adj2 is a superlative or comparative of adj1,
	vice versa
'''

############################################################
'''
	@Use: Find all instances of base, comparative, superlative
	      pairs from PPDB corpus
'''
def base_compare_super(root,edges,save):

	adjs = set(join([a,b] for a,b,_ in edges))

	'''
		initalize distinguished adverbs
	'''
	d_advs = {'intense': [], 'deintense': []}

	for w in adjs:
		w_er, w_est = compare_super(w)

		'''
			set of all advs that strengthens the weaker adjective
		'''	
		v_intense = [[a,b,v] for a,b,v in edges if \
		             a == w and b == w_er  or       \
		             a == w and b == w_est or       \
		             a == w_er and b == w_est       ]

		'''
			set of all advs that weakens the stronger adjective
		'''
		v_deintense = [[a,b,v] for a,b,v in edges if \
		               a == w_er  and b == w  or     \
	      	           a == w_est and b == w  or     \
	    	           a == w_est and b == w_er      ]

		'''
			set of all advs that is neutral
		'''
		v_neut  = [[a,b,v] for a,b,v in edges if \
		           a == w     and b == w     or  \
		           a == w_er  and b == w_er  or  \
		           a == w_est and b == w_est     ]


		d_advs['intense'  ] += v_intense
		d_advs['deintense'] += v_deintense

	if save:
		pathi  = os.path.join(root,'inputs/intense.txt')
		pathd  = os.path.join(root,'inputs/deintense.txt')
		fi     = open(pathi,'w')
		fd     = open(pathd,'w')

		save_list(fi,d_advs['intense'])
		save_list(fd,d_advs['deintense'])

	return d_advs

def compare_super(w):
	if w == 'good':
		return ['better','best']
	elif w == 'bad':
		return ['worse','worst']
	elif w == 'little':
		return ['less', 'least']
	elif w == 'much':
		return ['more', 'most']
	elif w == 'far':
		return ['farther', 'farthest']
	else:
		return [w + 'er', w + 'est']

############################################################
# Utils


strip       = lambda ls : (ls[0].strip(), ls[1].strip(), ls[2].strip())
split_comma = lambda xs : [ strip(x.split(',')) for x in xs if len(x.split(',')) == 3]
split_tab   = lambda xs : [ x.split('\t') for x in xs]

############################################################
# Depricated


# '''
# 	@Use: Given adjectives a1 a2, 
# 	      find all (a1,a2; v) and (a2,a1; v)
# 	      edges and look up value of v in words
# 	      solve Ax = b
# 	      where x = [a1,a2]
# '''
def run_test(root, a1, a2, all_edges, words):
	pass

# 	# Grab all paraphrase from graph
# 	a12v = [(a,b,v) for a,b,v in all_edges if a1 == a and a2 == b]
# 	a21v = [(a,b,v) for a,b,v in all_edges if a2 == a and a1 == b]

# 	'''
# 		Build A matrix and b vector
# 	'''
# 	A = [[-1,1]]*len(a12v) + [[1,-1]]*len(a21v)
# 	b = [words[v] for _,_,v in a12v + a21v ]

# 	'''
# 		Save as text file for matlab solver
# 	'''
# 	row_str = lambda r : ','.join([str(x) for x in r])
# 	A_path  = os.path.join(root,'outputs/A-matrix-' + a1 + '-' + a2 + '.txt')
# 	f       = open(A_path,'w')
# 	A_save  = [row_str(r) for r in A]

# 	save_list(f,A_save)
# 	f.close()

# 	b_path = os.path.join(root,'outputs/b-vector-' + a1 + '-' + a2 + '.txt')
# 	h      = open(b_path,'w')
# 	bstr   = '\n'.join(str(x) for x in b)
# 	h.write(bstr)
# 	h.close()

# 	return (A,b)







