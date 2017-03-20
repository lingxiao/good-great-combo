############################################################
# Module  : Eclectic IO scripts
# Date    : December 22nd
# Author  : Xiao Ling
# ############################################################

import os
import datetime

from ilp_scripts import * 
from prelude import *

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

############################################################

def save_ranking(results, root, name):

  print('\n>> saving ranking to ' + os.path.join(root, name))

  demark = '-'*50 + '\n'
  ranks  = results['ranking']

  with open(os.path.join(root,name + '.txt'),'w') as f:

    f.write(name + '\n')
    f.write(str(datetime.datetime.now()) + '\n')
    f.write(demark)

    for _,rank in ranks.iteritems():
      for w in rank['algo']:
        f.write(', '.join(w) + '\n')
      f.write(demark)
    f.write('=== END')


def save_results(results, root, name):

  print('\n>> saving file to ' + os.path.join(root, name))

  demark = '------------------------------------------------\n'

  ranking      = results['ranking']
  avg_taus     = results['tau']
  avg_abs_taus = results['|tau|']
  avg_pairwise = results['pairwise']

  with open(os.path.join(root,name + '.txt'),'w') as f:

    f.write(name + '\n')
    f.write(str(datetime.datetime.now()) + '\n')

    f.write(demark)
    f.write('average tau:  '      + str(round(avg_taus      ,2)) + '\n')
    f.write('average |tau|:'      + str(round(avg_abs_taus  ,2)) + '\n')
    f.write('average pairwise : ' + str(round(avg_pairwise*100)) + '%\n')
    f.write(demark)

    for _,rank in ranking.iteritems():
      
      f.write('=== tau:\n'               + str(rank['tau'])       + '\n\n')
      f.write('=== pairwise accuracy:\n' + str(rank['pairwise'])  + '\n\n')

      f.write('=== gold: \n')      
      for w in rank['gold']:
        f.write(str(w) + '\n')
      f.write('\n')

      f.write('=== algo: \n')      
      for w in rank['algo']:
        f.write(str(w) + '\n')
      f.write('\n')

      f.write(demark)

    if results['probs']:
      f.write('=== raw probs: \n')      
      for k,v in results['probs'].iteritems():
        f.write(str(k) + ': ' + str(v) + '\n')

    f.write('=== END')








