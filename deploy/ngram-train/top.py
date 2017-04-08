############################################################
# Module  : get google ngram lines for training data
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
from utils   import *
from scripts import *
from app.config import PATH

############################################################
'''
	paths

	read test-set
'''
ccb  = read_gold(PATH['assets']['ccb'])
moh  = read_gold(PATH['assets']['bansal'])

gr_path  = PATH['assets']['graph']
wt_path  = PATH['inputs']['graph-wt-by-edge']
ppr_path = PATH['inputs']['ppr-by-ppdb']
log_dir  = PATH['directories']['input']


'''
	working direcotry
'''
_root       = os.path.join(PATH['directories']['deploy'], 'ngram-train')
_pair_dir   = os.path.join(_root, 'pairs') 
_output_dir = os.path.join(_root, 'outputs')
_script_dir = os.path.join(_root ,'scripts')
_shell_dir  = os.path.join(_root ,'shells' )

############################################################
'''
	construct pairs where there is a known relationships
	give these precedant when collecting data
'''
G       = Graph(gr_path, wt_path, ppr_path)
train   = G.train()
G_pairs = list(set((s,t) for s,t,_ in train['graph']))

def test_set_pairs(gold):
	words = join(gold)
	pairs = [(s,t) for s in words for t in words if s != t]
	return pairs

ccb_pairs = join(test_set_pairs(gold) for _,gold in ccb.iteritems())
moh_pairs = join(test_set_pairs(gold) for _,gold in moh.iteritems())

pairs = G_pairs + ccb_pairs + moh_pairs

############################################################
'''
	@Use: split edges into chunks to compute
	      weight on remote 
'''
def split_into_pairs(size, pairs, output_dir):

	splits   = list(chunks(pairs, size))
	splits   = [splits[0][0:4]] + splits

	cnt = 0

	print('\n>> splitting words pairs into ' + str(len(splits)) + ' chunks')
	
	for ws in splits:

		path = os.path.join(output_dir, 'batch-' + str(cnt) + '.txt')

		with open(path,'wb') as h:
			for s,t in ws:
				h.write(s + ', ' + t + '\n')

		cnt += 1

	return cnt


'''
	@Use: rewrite main-#.py file
'''
def run_auto_main(tot):

	cnt = 1

	for k in xrange(tot-1):
		src_path = os.path.join(_root, 'main-0.py')
		tgt_path = os.path.join(_script_dir, 'main-' + str(cnt) + '.py')
		src_str  = 'batch = 0'
		tgt_str  = 'batch = ' + str(cnt)
		auto_gen(src_path, tgt_path, src_str, tgt_str)
		cnt += 1

'''
	@Use: rewrite main-#.sh file
'''
def run_auto_sh(tot):

	cnt = 1

	for k in xrange(tot-1):
		src_path = os.path.join(_root,'main-0.sh')
		tgt_path = os.path.join(_shell_dir,'main-' + str(cnt) + '.sh')
		src_str  = 'main-0'
		tgt_str  = 'main-' + str(cnt)

		auto_gen(src_path, tgt_path, src_str, tgt_str)

		cnt +=1

############################################################
'''
	run all
# '''
n = split_into_pairs(40, pairs, _pair_dir)
run_auto_main(n)
# run_auto_sh  (n)



