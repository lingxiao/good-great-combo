############################################################
# Module  : Make training and validations set
# Date    : January 22nd
# Author  : Xiao Ling
############################################################

import os
import re
import datetime
import operator
import random
import itertools
from copy import deepcopy
import numpy as np

from scripts import * 
from prelude import *

############################################################
'''
	PATHS
'''
root   = "/Users/lingxiao/Documents/research/code/good-great-ppdb"
iedges = os.path.join(root,'inputs/intense-copy.txt'  )
dedges = os.path.join(root,'inputs/deintense-copy.txt')
graph  = os.path.join(root,'inputs/raw/all_edges.txt' )
graph  = label_adv(split_comma(open(graph,'r' ).read().split('\n')))

'''
	get labeled pairs
'''
labeled_path  = os.path.join(root,'inputs/raw/pairwise_judgements.txt')
labeled_raw   = split_tab  (open(labeled_path,'r').read().split('\n'))[0:-1]

labeled_raw   = [(float(x),float(y),float(t),a1,a2)    \
                 for m,x,y,t,_,_,a1,a2 in labeled_raw       \
                 if unanimous(float(x),float(y),float(t))]

labeled  = list(set(mark_label(t) for t in labeled_raw))
labeled  = [(u,y,v) for u,y,v in labeled if y != '==']

'''	
	make training and test set
'''
n        = int(len(labeled)/2.0)
train    = labeled[0:n]
test     = labeled[n+1:-1]


'''
	save training and test set
'''
# f = open(os.path.join(root, '/inputs/train.txt'),'w')
# h = open(os.path.join(root, '/inputs/test.txt' ),'w')

# for u,y,v in train:
# 	f.write(u + '\t' + y + '\t' + v + '\n')
# f.close()

# for u,y,v in test:
# 	h.write(u + '\t' + y + '\t' + v + '\n')
# h.close()



