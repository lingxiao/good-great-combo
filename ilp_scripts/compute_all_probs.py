# ############################################################
# # Module  : Constructing all probability
# # Date    : December 22nd
# # Author  : Xiao Ling
# ############################################################

import os
import datetime

from ilp_scripts import * 
from scripts import * 
from prelude import *


'''
	@Use: given boolean flag `refresh`, if true:
			check to see if probability lookup table
			have been constructed
			if not then construct all graphs
			else do nothing
		 if not refresh, then construct all graphs
'''
# compute_all_probs :: Bool -> IO ()
def compute_all_probs(refresh):
	'''
		Paths
	'''

	root        = os.getcwd()
	input_dir   = os.path.join(root, 'inputs/raw')
	output_dir  = os.path.join(root, 'outputs/')


	ppdb_graph      = os.path.join(input_dir, 'ppdb-graph.txt'    ) 
	ppdb_graph_and  = os.path.join(input_dir, 'ppdb-graph-and.txt') 
	ppdb_graph_or   = os.path.join(input_dir, 'ppdb-graph-or.txt' ) 
	ngram_graph     = os.path.join(input_dir, 'ngram-graph.txt')

	print('\n>> opening all graphs')
	'''
		open all graphs
	'''
	ppdb_graph      = split_comma(open(ppdb_graph     ,'r' ).read().split('\n'))
	ppdb_graph_and  = split_comma(open(ppdb_graph_and ,'r' ).read().split('\n'))
	ppdb_graph_or   = split_comma(open(ppdb_graph_or  ,'r' ).read().split('\n'))
	ngram_graph     = label_adv(split_comma(open(ngram_graph,'r' ).read().split('\n')))


	print('\n>> naively combining all ppdb data with ngram data')
	'''
		combine all graphs with ngram graph
	'''
	combo_ppdb     = ppdb_graph     + ngram_graph
	combo_ppdb_and = ppdb_graph_and + ngram_graph
	combo_ppdb_or  = ppdb_graph_or  + ngram_graph

	############################################################
	'''
		get list of words in Veronica's graph
	'''
	words = list(set(join([u,v] for u,v,_ in combo_graph)))

	'''
		compute and save probability for both
		if file does not exit already
	'''
	name     = 'probs-combo-graph'
	name_and = 'probs-combo-graph-and'
	name_or  = 'probs-combo-graph-or'

	print('\n>> constructing all graphs')

	if not os.path.isfile(os.path.join(output_dir, name + '.txt')):
		probs_both(output_dir, name, words, combo_graph)

	if not os.path.isfile(os.path.join(output_dir, name_and + '.txt')):
		probs_both(output_dir, name_and, words, combo_graph_and)

	if not os.path.isfile(os.path.join(output_dir, name_or + '.txt')):
		probs_both(output_dir, name_or, words, combo_graph_or)











