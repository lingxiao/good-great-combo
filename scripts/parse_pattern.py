############################################################
# Module  : Translate paper's parser pattern syntax 
#           to regular expression
# Date    : January 15th, 2017
# Author  : Xiao Ling
############################################################

from utils import *
import string

############################################################
# Parse paper's regexp to python regexp
############################################################

def parse_pattern(pattern,words):
    ps = join(unpack_pattern(p) for p in pattern)
    qs = [fill_hole(p,words) for p in ps]
    return qs  
    # return zip(pattern, qs)

'''
    @Use: given pattern of form 
            "not just * but also *"
          fill in wildcards with words
'''

def fill_hole(pattern,words):
    out = ''
    w   = 0
    for p in pattern:
        if p != '*': out += p
        else       :
            out += words[w]
            w +=1
    return out

'''
    @Use: given pattern of form 
            "not just * (,) but also (a|an|the) *"
          upack it into phrases
'''
def unpack_pattern(pattern):

    wss     = [from_opt(x) for x in pattern.split(' ')]
    phrases = []

    for ws in wss:
        if type(ws) == str:
            if not phrases: phrases = [[ws]]
            else:
                phrases = [x + [ws] for x in phrases]
        if type(ws) == list:
            phrases1 = [p + [w] for p in phrases for w in ws]
            phrases  = phrases1
        
    patts = list(set(' '.join(p) for p in phrases))
    patts = [[p for p in ps.split(' ') if p] for ps in patts]
    return [' '.join(p) for p in patts]

############################################################

def opt(rs):
    return rs[0] == "(" and rs[-1] == ")"

def from_opt(rs):
    if not opt(rs): return rs
    else:
        ys = rs.split('|')
        return [x.replace('(','').replace(')','') for x in ys] + ['']


# join [[a]] -> [a]
def join(xxs):
	return [item for sublist in xxs for item in sublist]
