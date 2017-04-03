############################################################
# Module  : Read and write Gold IO scripts
# Date    : December 22nd
# Author  : Xiao Ling
# ############################################################

import os
import datetime

############################################################
'''
	@Use: read gold test set
'''
def read_gold(path):
	gold = open(path,'r').read().split('===')[1:-1]
	gold = [rs.split('\n') for rs in gold if rs.split('\n')]
	gold = [rs[1:-1] for rs in gold]
	gold = [(k,[r.split(', ') for r in val]) for k,val in enumerate(gold)]
	return dict(gold)

'''
  @Use: write gold test so that
        read_gold(p) == (write_gold q golds >>=\q -> read_gold(q))
'''
def write_gold(path, golds):
  with open(path) as h:
    for k,ws in golds.iteritems():
      h.write('=== ' + k + '\n')
      for w in ws:
        h.write(', '.join(w) + '\n')
    h.write('=== END')
    h.close()
    return path










