############################################################
# Module  : Load PPDB data from Veronica
# Date    : December 18th
# Author  : Xiao Ling
############################################################

import datetime
import os
from scripts import *
from prelude import *
from random  import shuffle
from copy    import deepcopy

############################################################
# Load Training Data

def load_training(root, label_path, graph_path):
	(strong, weak, neut) = prep_train(label_path, graph_path)
	(strong, weak, neut) = scrub_clusters(strong,weak,neut)

	# uncomment to save 
	# save(root, 'strong-train', strong)
	# save(root, 'weak-train'  , weak  )
	# save(root, 'neutral-train', neut )

	return {'train'  : permute_training(strong,weak,neut)
	       ,'strong' : strong
	       ,'weak'   : weak
	       ,'neutral': neut}

'''
	@Use: prep training data given to ppdb_data.txt and 
		  pairwise_judgements.txt where it has format:
		number of workers holding majority judgement (out of 3)  <tab>
		number of workers who think word1 is stronger than word2 <tab>
		number of workers who think word2 is stronger than word1 <tab>
		number of workers who think word1 and word2 are equal    <tab>
		adjective cluster 										 <tab>
		cluster ID number										 <tab>
		word1 													 <tab>
		word2 <newline>
	@Output: dictionary where:
				cluster_id : strong  : (ai,aj) : [adverbs]
				             weak    : ...
				             netural : ...
'''
def prep_train(cl_path, mat_path):
	
	adj_mat      = load_adjacency_matrix(mat_path)
	raw_clusters = open(cl_path,'r').read().split('\n')
	raw_clusters = [c.split('\t') for c in raw_clusters][0:-1]
	raw_clusters = [[float(a),int(s),int(w),int(n),b,float(c),a1,a2] \
	                for [a,s,w,n,b,c,a1,a2] in raw_clusters if a1 != a2]


	num_clusters = max(int(x[5]) for x in raw_clusters)

	cluster_strong = dict()
	cluster_weak   = dict()
	cluster_neut   = dict()

	for [_,s,w,n,cn,cid,a1,a2] in raw_clusters:

		if (a1,a2) in adj_mat: adverbs1 = adj_mat[(a1,a2)]
		else                 : adverbs1 = []
		if (a2,a1) in adj_mat: adverbs2 = adj_mat[(a2,a1)]
		else                 : adverbs2 = []

		if adverbs1 or adverbs2:

			if s > w and s > n:

				cluster_strong[(a1,a2)] = {a1    : adverbs1
				                          ,a2    : adverbs2
				                          ,'id'  : cid
				                          ,'rank': a1 + ' > ' + a2}

			elif w > s and w > n:
				cluster_weak[(a1,a2)] = {a1    : adverbs1
     			                        ,a2    : adverbs2
				                        ,'id'  : cid
				                        ,'rank': a1 + ' < ' + a2}

			elif n > w and n > s:
				cluster_neut[(a1,a2)] = {a1    : adverbs1
				                        ,a2    : adverbs2
				                        ,'id'  : cid
				                        ,'rank': a1 + ' = ' + a2}

	# return dclusters
	return (cluster_strong, cluster_weak, cluster_neut)

'''
	randomly permute the training data
'''
def permute_training(strong,weak,neut):

	items = [(aij,strong[aij]) for aij in strong] \
		  + [(aij,weak[aij]  ) for aij in weak  ] \
		  + [(aij,neut[aij]  ) for aij in neut  ]  

	for k in range(1,100):
		shuffle(items)
	
	train = dict()

	for (ai,aj),d in items:
		train[(ai,aj)] = d

	return train

def save_training(root, name, cluster):

	path = os.path.join(root, name + '.txt')

	f = open(path,'w')
	f.write(name + '\n')
	f.write(str(datetime.datetime.now()) + '\n')
	f.write(demark)

	for (ai,aj),d in cluster.iteritems():
		f.write('=== ' + ai + ', ' + aj + '\n\n')
		f.write(d['rank'] + '\n')
		f.write('cluster id: ' + str(d['id']) + '\n\n')  

		f.write('modifying ' + ai + ':\n')
		save_list(f, d[ai])
		f.write('modifying ' + aj + ':\n')
		save_list(f, d[aj])
		f.write(demark)

	f.close()


'''
	@Use: santitize the training data by tossing out
	      contradictory ranking given by mechanical turks:
		      If pair (ai,aj) appears in netural and 
		      appear in strong or weak with the same
		      cluster id, then we remove it from neutral

'''
def scrub_clusters(strong,weak,neut):
	
	strong_neut = []
	strong_weak = []
	weak_neut   = []

	for (ai,aj), d in strong.iteritems():
		if (ai,aj) in weak and d['id'] == weak[(ai,aj)]['id']:
			strong_weak.append((ai,aj))
		if (ai,aj) in neut and d['id'] == neut[(ai,aj)]['id']:
			strong_neut.append((ai,aj))

	for (ai,aj),d in weak.iteritems():
		if (ai,aj) in neut and d['id'] == neut[(ai,aj)]['id']:
			weak_neut.append((ai,aj))

	strong1 = deepcopy(strong)
	weak1   = deepcopy(weak  )
	neut1   = deepcopy(neut  )

	for ai,aj in strong_neut:
		del strong1[(ai,aj)]
		del neut1  [(ai,aj)]

	for ai,aj in strong_weak:
		del strong1[(ai,aj)]	
		del weak1  [(ai,aj)]

	for ai,aj in weak_neut:	
		del weak1  [(ai,aj)]
		del neut1  [(ai,aj)]

	return (strong,weak,neut)


'''
	@Use: prepare adverb sets by:
	      for every a1 < a2 pair, we take
	      the adverbs modifying a1 and 
	      push them into the intensifying list
	      and take adverbs modifying a2 and
	      push them into de-intensifying list

	      for every a1 = a2, we take 
	      adverbs modfying a1 and those modifying 
	      a2 and push them into neutral list

'''
def adverb_hits(train,strong,weak,neut):

	adverbs = to_adverbs(train)

	for v in adverbs:

		d = {'intense': [],'deintense': [], 'neutral': []}

		'''
			count the number of times
			  - v is used as a intensifying adverb
			  - v is used as a de-intensifying adverb
			  - v is neutral

		'''	
		for (s,w),data in strong.iteritems():
			if v in data[s]: 
				d['intense'].append(w)
			if v in data[s]:
				d['deintense'].append(s)

		for (w,s), data in weak.iteritems():
			if v in data[w]:
				d['intense'].append(w)
			if v in data[s]:
				d['deintense'].append(s)


		for (a,b), data in neut.iteritems():
			if v in data[a]:
				d['neutral'].append(a)
			if v in data[b]:
				d['neutral'].append(b)

		adverbs[v] = d

	return adverbs

	# name = 'adverb-hits'
	# path = os.path.join(root, name + '.txt')
	# f    = open(path,'w')

	# f.write(name + '\n')
	# f.write(str(datetime.datetime.now()) + '\n')
	# f.write(demark)

	# for v,d in adverbs.iteritems():
	# 	f.write('***** ' + v + '\n')
	# 	for key,lst in d.iteritems():
	# 		f.write('=== ' + key + ', counts: ' \
	# 			    + str(len(lst)) + ':\n')
	# 		save_list(f,lst)

	# f.write('\n=== END')
	# f.close()

############################################################
# Load Adjacency matrix 

'''
	@Use: Given a handle f and list xs,
	      save all items of list in new lines
'''
def save_adjacency_matrix(mat,name,root):
	
	path = os.path.join(root  ,name + '.txt')
	f    = open(path,'w')

	f.write(name + '\n')
	f.write(str(datetime.datetime.now()) + '\n')
	f.write(demark)

	for ai,aj in mat:
		f.write('=== ' + ai + ', ' + aj + '\n')
		save_list(f,mat[(ai,aj)])

	f.write('\n=== END')
	f.close()

'''	
	@Use: Load ppdb_data.txt, an alternate
	      format to veronica's data, but
	      with the same content

	@Output: a dictionary with the following format:
		(ADJ1, ADJ2): [ADVERB_i]
		interpreted as "ADVERB_i ADJ1 <=> ADJ2" for every i 
		For example, limited,restricted,quite means 
		that "quite limited" is a 
		paraphrase for "restricted"		

'''
def load_adjacency_matrix(mat_path):

	mat = open(mat_path,'r').read()
	mat = mat.split('===')[1:-1]
	mat = [m.split('\n') for m in mat]
	mat = [(m[0].split(','),m[1:]) for m in mat]

	matrix = dict()

	for ([ai,aj],advs) in mat:
		ai   = ai.strip()
		aj   = aj.strip()
		hits = [a for a in advs if a]
		matrix[(ai,aj)] = hits

	return matrix

############################################################
# load veronica's data

'''
	@Use: load veronica's data and massage
	      into a dictionary where:
		Each key is a pair of adjectives (ai,aj)
		and it is populated by a list of words that
		connects two adjectives
		The file has the format 
		ADJ1, ADJ2, ADVERB, 
		interpreted as "ADVERB ADJ1 <=> ADJ2". 
		For example, limited,restricted,quite means 
		that "quite limited" is a 
		paraphrase for "restricted"		
'''
def load_raw_data(adj_path, edge_path):

	adj = open(adj_path,'r').read()
	adj = adj.split('\n')

	raw  = open(edge_path,'r').read()
	raw  = [e.split(',') for e in raw.split('\n')]
	raw  = [[x for x in e if x] for e in raw]
	raw1 = [e for e in raw if len(e) == 3] 

	# TODO: ask veronica what to do with this:
	raw2 = [e for e in raw if len(e) != 3] 

	adjacency_mat = dict()

	for ai,aj,adv in raw1:
		if (ai,aj) not in adjacency_mat:
			adjacency_mat[(ai,aj)] = [adv]
		else:
			adjacency_mat[(ai,aj)].append(adv)

	return adjacency_mat



def to_adverbs(train):

	adverbs = []

	for (ai,aj),d in train.iteritems():
		adverbs.append(d[ai])
		adverbs.append(d[aj])

	keys = list(set(join(adverbs)))

	return dict.fromkeys(keys)

############################################################
# utils

def save_list(f,xs):
	for x in xs:
		if not isinstance(x,str):
			x = str(x)
		f.write(x + '\n')
	f.write('\n')

demark = '-'*50 + '\n'











