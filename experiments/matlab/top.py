############################################################
# Module  : base compare and superlative adjectives
# Date    : December 22nd
# Author  : Xiao Ling
# Source  : http://www.enchantedlearning.com/grammar/partsofspeech/adjectives/comparatives.shtml
############################################################

import os
from nltk.stem.wordnet import WordNetLemmatizer

from utils import *
from app.config import *

############################################################
'''
	Load assets from paths
'''
# G :: [(String,String,String)]
# w :: [String]
G,words = load_as_list(PATH['assets']['graph'])

# A0,b0,x_lookup0 = to_Ab(subgraph0,known0)

############################################################
'''
	construct subgraph with all base, comparatives, and superlative forms
'''
G_base_compare    = [(s,t,v) for s,t,v in G if base_compare(s,t)   ]
G_compare_base    = [(s,t,v) for s,t,v in G if compare_base(s,t)   ]
G_base_superla    = [(s,t,v) for s,t,v in G if base_superla(s,t)   ]
G_superla_base    = [(s,t,v) for s,t,v in G if superla_base(s,t)   ]
G_compare_superla = [(s,t,v) for s,t,v in G if compare_superla(s,t)]
G_superla_compare = [(s,t,v) for s,t,v in G if superla_compare(s,t)]

subgraph = G_base_compare        \
         + G_compare_superla     \
         + G_base_superla        \
         + G_superla_base        \
         + G_compare_superla     \
         + G_superla_compare

############################################################
'''
	get all base compare and superla forms from graph
'''
base = set([s for s,_,_ in G_base_compare] \
	     + [t for _,t,_ in G_compare_base] \
	     + [s for s,_,_ in G_base_superla] \
	     + [t for _,t,_ in G_superla_base])


compare = set([x for _,x,_ in G_base_compare] \
		     + [x for x,_,_ in G_compare_base] \
		     + [x for x,_,_ in G_compare_superla] \
		     + [x for _,x,_ in G_superla_compare])


superla = set([x for _,x,_ in G_base_superla] \
		     + [x for x,_,_ in G_superla_base] \
		     + [x for _,x,_ in G_compare_superla] \
		     + [x for x,_,_ in G_superla_compare])











