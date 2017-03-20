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

############################################################

def save(results, root, name):

  demark = '------------------------------------------------\n'

  ranking      = results['ranking']
  avg_taus     = results['tau']
  avg_abs_taus = results['|tau|']
  avg_pairwise = results['pairwise']


  f    = open(os.path.join(root,name + '.txt'),'w')
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

    f.write('=== raw score: \n')      
    for w in rank['raw-score']:
      f.write(str(w) + ': ' 
                     + str(rank['raw-score'][w]) + '\n')
    f.write('\n')


    f.write(demark)


  f.close()









