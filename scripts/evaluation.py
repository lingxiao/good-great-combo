############################################################
# Module  : Kendall's tau correlation coefficient
# Date    : November 6th
# Author  : Xiao Ling
############################################################

from prelude import * 
from math import * 

############################################################
# Pairwise acuracy

def pairwise_accuracy(gold,algo):
  words = join(gold)
  pairs = unique_pairs(words)

  correct = [(u,v) for u,v in pairs \
            if agree(u,v,gold,algo)]

  return float(len(correct))/len(pairs)

def agree(ai,ak,gold,algo):
  return greater(ai,ak,gold) and greater(ai,ak,algo) \
  or     lesser (ai,ak,gold) and lesser (ai,ak,algo) \
  or     equal  (ai,ak,gold) and equal  (ai,ak,algo) 


############################################################
# Kendall's Tau 
'''
	@Input : `xs` Gold standard list of list of words 
	         every word in each list_i in `xs` is 
	         the same intensity, and less than every word
	         in list_j in `xs` if i < j
	         `ys` same list of words ranked according to 
	          paper's milp algorithm
	@Output: Kendall's tau score where:

	                                     P - Q
	          tau =        -------------------------------------
	                            ------------------------------
	                          \/ (P + Q + X0) * (P + Q + Y0)



	          Alternate measure for tau, suppose we are to rank
	          n words, then:

	                  # of concordant pairs - # of discordant pairs
            tau2 =   -------------------------------------------------
                                    n*(n-1)/2

'''
# tau :: [[String]] -> [[String]] -> Float
def tau(gold,algo):

  if not gold:
    raise NameError('Empty list gold')

  if not algo:
    raise NameError('Empty list algo')

  pairs = unique_pairs(join(gold))
  p     = [(u,v) for u,v in pairs if concordant(u,v,gold,algo)]
  q     = [(u,v) for u,v in pairs if discordant(u,v,gold,algo)]
  x     = [(u,v) for u,v in pairs if equal     (u,v,gold)     ]
  y     = [(u,v) for u,v in pairs if equal     (u,v,algo)     ]


  P     = float(len(p))   # concordant
  Q     = float(len(q))   # discordant
  X     = float(len(x))   # gold ties
  Y     = float(len(y))   # our ties

  top   = P - Q

  '''
  	in this version we account for ties
  '''
  bot = sqrt((P + Q + X)*(P + Q + Y))

  '''
    If we only output ties, then 
    defult to 0
  '''
  if not bot: return 0.0
  else: return top / bot


def tau2(gold,algo):
  pairs = unique_pairs(join(gold))
  p     = [(u,v) for u,v in pairs if concordant (u,v,gold,algo)]
  q     = [(u,v) for u,v in pairs if discordant2(u,v,gold,algo)]

  P     = float(len(p))   # concordant
  Q     = float(len(q))   # discordant


  top   = P - Q

  '''
    in this version we ignore ties
    note length (pairs) = n * (n-1)/2
  '''
  bot = float(len(pairs))

  return top / bot


def concordant(ai,ak,gold,algo):
  return greater(ai,ak,gold) and greater(ai,ak,algo) \
  or     lesser (ai,ak,gold) and lesser (ai,ak,algo) \

def discordant(ai,ak,gold,algo):
  return greater(ai,ak,gold) and lesser (ai,ak,algo) \
  or     lesser (ai,ak,gold) and greater(ai,ak,algo) \

def discordant2(ai,ak,gold,algo):
  return greater(ai,ak,gold) and lesser (ai,ak,algo) \
  or     lesser (ai,ak,gold) and greater(ai,ak,algo) \
  or     equal  (ai,ak,gold) and greater(ai,ak,algo) \
  or     equal  (ai,ak,gold) and lesser (ai,ak,algo) \


############################################################
# Utils

# greater :: String -> String -> [(String,String)] -> Bool
def greater(ai,ak,gold):
  ii = -1
  ki = -1
  for idx in range(0,len(gold)):
    if ai in gold[idx]: ii = idx
    if ak in gold[idx]: ki = idx

  return ii > ki

# same :: String -> String -> [(String,String)] -> Bool
def equal(ai,ak,gold):
  ts = [ai in rw and ak in rw for rw in gold]
  return any_(lambda x: x == True, ts)

# lesser :: String -> String -> [(String,String)] -> Bool
def lesser(ai,ak,gold):
  return not equal(ai,ak,gold) and not greater(ai,ak,gold)

def unique_pairs(words):
  if not words: return []
  else:
    v  = words[0]
    ws = words[1:]
    return [(v,w) for w in ws] + unique_pairs(ws)




############################################################
# Spearman's rho

# @Input : `xs` Gold standard list of list of words 
#          every word in each list_i in `xs` is 
#          the same intensity, and less than every word
#          in list_j in `xs` if i < j
#          `ys` same list of words ranked according to 
#           paper's milp algorithm
# @Output: Spearman's rho score, where:
# 
# 
# spearman_rho :: [[String]] -> [[String]] -> Float
def spearman_rho(xs,ys):
	pass