############################################################
# Module  : base compare and superlative adjectives
# Date    : December 22nd
# Author  : Xiao Ling
# Source  : http://www.enchantedlearning.com/grammar/partsofspeech/adjectives/comparatives.shtml
############################################################

import unittest
from utils import *

############################################################
'''
	special cases: irregular cases of base, comparative, and superlative adjectives
'''
special_base_compare = [('good' , 'better' )
				        ,('well' , 'better' )
				        ,('ill'  , 'worse'  )
				        ,('bad'  , 'worse'  )
				        ,('happy', 'happier')
				        ,('busy' , 'busier' )
				        ,('little', 'less'  )
				        ,('many'  , 'more'  )
				        ,('much'  , 'more'  )
				        ,('some'  , 'more'  )
				        ,('far'   , 'farther')
				        ,('far'   , 'further')
				        ,('old'   , 'elder' )]

special_compare_superla = [('better' , 'best'    )
			                ,('better' , 'best'    )
			                ,('worse'  , 'worst'   )
			                ,('worse'  , 'worst'   )
			                ,('happier', 'happiest')
			                ,('busier' , 'busiest' )
			                ,( 'less'  , 'least'   )
			                ,( 'more'  , 'most'    )
			                ,( 'more'  , 'most'    )
			                ,( 'more'  , 'most'    )
			                ,( 'farther', 'farthest')
			                ,( 'further', 'furthest')
			                ,( 'elder'  , 'eldest'  )]

special_base_superla = [(s,t) for (s,x),(y,t) in \
                       zip(special_base_compare, special_compare_superla)\
                       if x == y]			                

############################################################
'''
	@Use: given words s and t, determine if
	      s is base form of t or t is base form of s
'''
def base_compare(s,t):

	# base case
	case1 = s + 'er' == t

	# last letter is 'e'
	case2 = s[-1] == 'e' and s + 'r' == t

	# last letter is consonent
	case3 = s + s[-1] + 'er' == t 

	# last letter is 'y'
	case4 = s[:-1] + 'ier' == t 

	return (s != t) and (case1 or case2 or case3 or case4 or (s,t) in special_base_compare)


def compare_base(s,t): 
	return base_compare(t,s)


'''
	@Use: given words s and t, determine if
	      s is base form of t or t is base form of s
'''
def base_superla(s,t):
	# base case
	case1 = s + 'est' == t 

	# last letter is 'e'
	case2 = s[-1] == 'e' and s + 'st' == t 

	# last letter is consonent
	case3 = s + s[-1] + 'est' == t 

	# last letter is 'y'
	case4 = s[:-1] + 'iest' == t 

	return (s!= t) and (case1 or case2 or case3 or case4 or (s,t) in special_base_superla)

def superla_base(s,t):
	return base_superla(t,s)

	
'''
	@Use: given words s and t, determine if
	      s is base form of t or t is base form of s
'''
def compare_superla(s,t):
	# base case
	case1 =  s[-2:] == 'er' and t[-3:] == 'est' 

	return (s != t) and (case1 or (s,t) in special_compare_superla)

def superla_compare(s,t):
	return compare_superla(t,s)

############################################################

'''
	unit test
'''
def unit_test():
	base    = ['close','big','dry', 'fast', 'fickle', 'bumpy','able'] \
	        + [s for s,_ in special_base_compare]

	compare = ['closer','bigger','drier', 'faster','fickler','bumpier', 'abler'] \
	        + [t for _,t in special_base_compare]

	superla = ['closest','biggest','driest', 'fastest', 'ficklest', 'bumpiest','ablest'] \
	        + [t for _,t in special_base_superla]

	for b,c in zip(base,compare):
		assert base_compare(b,c) == True
		assert base_compare(c,b) == False
		assert base_superla(b,c) == False
		assert base_superla(c,b) == False
		assert compare_superla(b,c) == False
		assert compare_superla(c,b) == False
	print('\n>> passed all base-compare word tests!')

	for b,s in zip(base,superla):
		assert base_compare(b,s) == False
		assert base_compare(s,b) == False
		assert base_superla(b,s) == True
		assert base_superla(s,b) == False
		assert compare_superla(b,s) == False
		assert compare_superla(s,b) == False
	print('\n>> passed all base-superla word tests!')

	for c,s in zip(compare,superla):
		assert base_compare(c,s) == False
		assert base_compare(s,c) == False
		assert base_superla(c,s) == False
		assert base_superla(s,c) == False
		assert compare_superla(c,s) == True
		assert compare_superla(c,c) == False
	print('\n>> passed all compare-superla word tests!')
	

























