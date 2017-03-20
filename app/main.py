# ############################################################
# # Module  : Applicaton Main
# # Date    : December 22nd
# # Author  : Xiao Ling
# ############################################################

import os
import datetime

from pulp import *
from app import *
from ilp_scripts import * 
from prelude import *

############################################################
'''
	Paths
'''
root        = os.getcwd()
test_dir    = os.path.join(root, 'inputs/testset')
output_dir  = os.path.join(root, 'outputs/')

cluster_1 = os.path.join(test_dir, 'cluster100.adj-adj.k25.txt' )
cluster_2 = os.path.join(test_dir, 'cluster500.adj-adj.k125.txt')

gold_moh    = os.path.join(root, 'inputs/testset/testset-bansal.txt')
gold_ccb    = os.path.join(root, 'inputs/testset/testset-ccb.txt')

############################################################
'''
	construct or open probs table
'''
# to_probs_table(refresh=True)

ngram_old_ppdb_probs = open_probs_table(os.path.join(output_dir, 'ngram-ppdb-old.txt'))
# ngram_ppdb_probs     = open_probs_table(os.path.join(output_dir, 'probs-ngram-ppdb.txt'))
# ngram_and_probs      = open_probs_table(os.path.join(output_dir, 'probs-ngram-ppdb-and.txt'))
# ngram_ppdb_or_probs  = open_probs_table(os.path.join(output_dir, 'probs-ngram-ppdb-or.txt'))

'''
	open clusters
'''
cluster1 = read_gold(cluster_1)
cluster2 = read_gold(cluster_2)
moh      = read_gold(gold_moh)
ccb      = read_gold(gold_ccb)

############################################################
'''
	run ilp on all clusters from anne

	where you left off: make sure what you have as
	an ilp works on chris's and mohit's data
'''

rmoh = ilp(ngram_old_ppdb_probs, moh)
rccb = ilp(ngram_old_ppdb_probs, ccb)


