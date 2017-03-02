############################################################
# Module  : Applicaton Main
# Date    : December 22nd
# Author  : Xiao Ling
############################################################

import os
import re
import datetime
from random import shuffle
from copy import deepcopy
from server  import * 
from prelude import *

############################################################
# Paths

name      = 'adj_mat'

root      = "/Users/lingxiao/Documents/research/code/good-great-ppdb"
inputs    = os.path.join(root,'inputs'         )
mat_path  = os.path.join(inputs,'ppdb_data.txt')
cl_path   = os.path.join(inputs,'pairwise_judgements.txt')

adj_mat = load_adjacency_matrix(mat_path)

d       = load_training(root,cl_path,mat_path)
train   = d['train']

############################################################
# construct feature embedding

'''
	@Use: pass through all training data
	      and update the weights
	@Input: training data in form, for example:
	            (adjective1, adjective2):
	            	adjective1: [adverbs]
	            	adjective2: [adverbs]
	            	rank      : adjective1 > adjective2
	            	id        : 1.0

	        weights mapping adverb to their value in [-1,1]
	        eps a learning parameter
'''
def step(train,weights,eps):

	for (ai,aj),data in train.iteritems():


		'''
			interepret data
		'''
		y       = label  (data)

		phi_ai  = embed(weights,data[ai])
		phi_aj  = embed(weights,data[aj])
		yhat    = dot(weights, phi_ai) - dot(weights,phi_aj)

		if sign_eps(yhat,eps) != y: 
			'''
				ai > aj
				thus adverbs modifying ai are 
				deintensifying adverbs,

				and we increment their value
				so phi(ai)*weights increases

				and adverbs modifying aj are 
				intensifying adverbs

				and we decrement their value
				so phi(aj)*weights decreses
			'''
			if y == 1:  
				incr    = mult(phi_ai, eps)
				decr    = mult(phi_aj, -eps)
				delta   = add (incr  , decr)

				weights = add (weights, delta)

			'''
				ai < aj
				thus adverbs modifying aj are 
				deintensifying adverbs,

				and we increment their value
				so phi(aj)*weights increases

				and adverbs modifying ai are 
				intensifying adverbs

				and we decrement their value
				so phi(ai)*weights decreses
			'''
			if y == -1:
				decr    = mult(phi_ai, -eps)
				incr    = mult(phi_aj, eps )
				delta   = add (incr  , decr)
				weights = add (weights, delta)

			'''
				ai = aj
				thus adverbs modifying aj are 
				neutral adverbs,
				and adverbs modifying ai are 
				neutral adverbs

				we bring them closer to zero by eps

			'''
			if y == 0:
				vs = [v for v in phi_ai] \
				   + [v for v in phi_aj]

				for v in vs:
					if sign_eps(weights[v],eps) < 0: weights[v] + eps
					if sign_eps(weights[v],eps) > 0: weights[v] - eps
	
	return weights

# basis   = init(train)
# weights = deepcopy(basis)
# eps     = 1.0/len(basis) * 20

# weights1 = step(train,weights,eps)

def learn(train,epochs):


	'''
		initalize stride rate and basis, and weights
	'''
	weights = init(train)
	eps     = 1.0/len(weights) * 80

	for k in range (0,epochs):
		weights = step(train,weights,eps)

		err     = error(train,weights,eps)

		print ('== current error rate: ', float(len(err))/len(train))

	return weights

def error(train, weights,eps):

	err = []

	for (ai,aj),data in train.iteritems():
		y       = label   (data)
		yhat    = predict (weights,data,ai,aj)
	 
		if sign_eps(yhat,eps) == y: pass
		else                      : err.append((ai,aj))

	return err

############################################################
# Initalization and embedding


def predict(weights, data, ai, aj):
	phi_ai  = embed(weights,data[ai])
	phi_aj  = embed(weights,data[aj])
	yhat    = dot(weights, phi_ai) - dot(weights,phi_aj)
	return yhat


'''
	initalize adverbs from training data
	set all adverbs to 0
'''
def init(train):

	adverbs = []

	for (ai,aj),d in train.iteritems():
		adverbs.append(d[ai])
		adverbs.append(d[aj])

	keys = set(join(adverbs))

	return dict(zip(keys,[0.0]*len(keys)))

'''
	embedd adjective into space
'''
def embed(basis,adverbs):
	o = dict()
	for v in basis:
		if v in adverbs: o[v] = 1.0
		else:            o[v] = 0.0
	return o

'''
	interepret ranking:
	    a1 > a2  => y = 1
	    a1 = a2  => y = 0
	    a1 < a2  => y = -1

'''
def label(data):
	xs      = data['rank']
	[_,r,_] = xs.split(' ')
	if r == '='  : return 0.0
	elif r == '>': return 1.0
	else         : return -1.0

###########################################################
# vector primitives
 
 # clip x to be between [-1,1]
def clip(x):
	return max(-1,(min(1,x)))

# vector multiply scalar
def mult(v,a):
	w = dict()
	for key in v:
		w[key] = v[key]*a
	return w

# vector dot product 
# @Use: given two vectors of same length, output value
# dot :: Dict String Float -> Dict String Float -> Float
def dot(u,v):
    return sum([u[key]*v[key] for key in u])

# element-wise vector addition with constraint
#  that the result is between -1 and 1
def add(u,v):
    o = dict()
    for key in u:
        x = u[key] + v[key]
        o[key] = x
        # o[key] = max(-1,(min(1,x)))
    return o

# element-wise vector subtraction: a - b
def sub(u,v):
    o = dict()
    for key in u:
        o[key] = u[key] - v[key]
    return o

# sign :: Float -> Bool
def sign(x):
    return x > 0

def sign_eps(x,eps):
	if   x > eps   : return 1
	elif x < -eps  : return -1
	elif x <= eps and x >= -eps: return 0

# @Use: given vec that is a tuple of floats,
#       convert it to a dictionary mapping string index to float
def to_vector(vec):
    i = 1
    d = dict()
    for x in vec:
        xi = 'x' + str(i)
        d[xi] = x
        i +=1 
    return d
