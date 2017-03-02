############################################################
# Module  : Applicaton Main
# Date    : December 22nd
# Author  : Xiao Ling
############################################################

import os
import datetime
from scripts import * 
from prelude import *

############################################################
# construct oracle


'''
	Poor man's ADT
'''
LABEL = ['<neutral>', '<intense>', 'neutral']


'''
	@Use: given directory to turk-labels label_dir
	      and ppdb paraphrase edge_dir

		construct dictionary of form:
			adverb: [(ai, aj, label)]
		where label \in {<, >, =}
		signifying whether ai < aj, ai > aj, or ai = aj

	@output: dictionary. save data
'''
# oracle :: FilePath -> FilePath 
#        -> IO (LABEL, Dict String [(Word, Word, String, LABEL)]))
def oracle(label_dir, edge_dir):

	'''
		load turk-labeled data and ppdb data
	'''
	(labels, edges) = load_edge_label(label_dir, edge_dir)

	data = dict()

	for [s,w,t,_,_,u,v] in labels:

		'''
			map (s,w,t) into '<' or '>' or '='
		'''
		(po, label) = interpret_score(s,w,t)

		'''
			load all adverbs found in document `edges` so that
			adverb u  paraphrases v
		'''
		advs = [adv for [a1,a2,adv] in edges if a1 == u and a2 == v]

		'''
			construct data of form:
				adverb: [(ai, aj, label)]
			where label \in {<, >, =}
			signifying whether ai < aj, ai > aj, or ai = aj
		'''
		for adv in advs:
			y = (u, v, po, label)
			if adv in data:	data[adv].append(y)
			else          :	data[adv] = [y]

	'''
		write to project root
	'''
	# save_oracle(data)

	return (LABEL, data)

############################################################
# Helpers

def load_edge_label(label_dir, edge_dir):
	'''
		load turk-labeled data and ppdb data
	'''
	labels = open(label_dir, 'r').read().split('\n')
	labels = [l.split('\t') for l in labels][0:-1]
	labels = [[int(a),int(b),int(c),d,e,f,g] for [k,a,b,c,d,e,f,g] \
	         in labels if float(k) >= 2.0]

	edges   = open(edge_dir, 'r').read().split('\n')
	edges   = [e.split(',') for e in edges][0:-1]
	edges   = [e[0:3] for e in edges]
	edges   = [[a.strip(), b.strip(), v.strip()] for [a,b,v] in edges]

	return (labels, edges)


'''
	read the three numbers in pairwise_judgements
	and output the order of inequality, or equality
'''
def interpret_score(s,w,t):
	if s > w and s > t  : return ('>', LABEL[-1])
	elif w > s and w > t: return ('<', LABEL[1])
	elif t > s and t > s: return ('=', LABEL[0])
	else: raise NameError(s,w,t)

demark = '-'*50 + '\n'

def save_oracle(root,data):
 	path = os.path.join(root,'oracle.txt')
	f    = open(path,'w')
	f.write('oracle' + '\n')
	f.write(str(datetime.datetime.now()) + '\n')
	f.write(demark)

	for adv,d in data.iteritems():
		f.write ('=== ' + adv + '\n\n')
		for u,v,sign,label in d:
			f.write(u + ' ' + sign + ' ' + v + ', ' + label)
			f.write('\n')
		f.write(demark)

	f.close()	


def save_data_adj(test_data):
	path = os.path.join(root,'test_data_adj.txt')
	f    = open(path,'w')

	f.write('test_data_adj\n')
	f.write(str(datetime.datetime.now()) + '\n')
	f.write(demark)

	for (u,v),d in test_data.iteritems():
		f.write('=== ' + u + ', ' + v + '\n\n')
		f.write(u + ' ' + d['order'] + ' ' + v + '\n\n')
		f.write('** ' + u + '-adverbs: \n')
		save_list(f, d[u])
		f.write('** ' + v + '-adverbs: \n')
		save_list(f, d[v])
		f.write(demark)
	f.close()	

def save_list(f,xs):
	for x in xs:
		if not isinstance(x,str):
			x = str(x)
		f.write(x + '\n')
	f.write('\n')




















