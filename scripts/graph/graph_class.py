############################################################
# Module  : Graph Class
# Date    : April 3rd, 2017
# Author  : Xiao Ling, merle
############################################################

from scripts.graph import *

'''

	Graph class and associated functions. 


	Class parameters:

	* graph_path :: String, path to multi-directed graph to be loaded
	* wt_dirh    :: String, path to directory with graph edge so it can be represented
	                 as a directed-graph

	Class methods:

	- edge :: String -> String -> [(String, String, String)] 
	         given vertices s and t, output all edges in s,t as list of : (s, t, adverb)

	- wtedge :: String -> String -> Float
	        given vertices s and t, output weight of edge s -> t
	        if no edge exist, output 0


	- mgraph :: [(String, String, String)]
	        output entire raw multi directed graph in list of tuples of form: (s,t,adverb)
	        where (s,t,adverb) signals:

			s + adverb = t

	- ppr :: String -> Float -> Dict String Float. 
	        compute the personalized page rank of vertex s at reset constant alpha

	- ppr_vec :: String -> Dict String Float
			compute personalized page rank of t from s for every t

	- train :: { 'graph' :: [(String,String,String)], 'base' :: String, 'compare' :: String, 'superla' :: String}
	          output partial graph with base, comparative, superlative vertices and their edges

'''

class Graph:

	def __init__(self, graph_path, weight_dir, ppr_dir):

		if os.path.exists(graph_path) and \
			os.path.exists(weight_dir) and \
			os.path.exists(ppr_dir):

			G,words = load_as_digraph(graph_path, weight_dir)
			mG, _   = load_as_list   (graph_path)

			self.PATH = {'graph' : graph_path
			           , 'weight': weight_dir
			           , 'ppr'   : ppr_dir}

			self.digraph   = G
			self.words     = words
			self.raw_graph = mG
			self._train    = None

		else:
			raise NameError('Error: ' + graph_path + ' and/or ' + weight_dir + ' does not exist')

	def edge(self,s,t):

		mG = self.raw_graph

		return [(x,y,z) for x,y,z in mG if s == x and y == t]

	def wtedge(self, s, t):
		G = self.digraph
		if s in G:
			if t in G[s]: return G[s][t]['weight']
			else: return 0
		else:
			raise NameError('vertex ' + s + ' not found here')

	def train(self):

		if self._train:
			return self._train
		else:
			t = training_graph(self.raw_graph)
			self._train = t
			return t

	def ppr(self,s,t, alpha):

		ppr_dir = self.PATH['ppr']
		name = s + '-' + str(alpha) + '.pkl'
		path = os.path.join(ppr_dir,name)

		if os.path.exists(path):
			ppr_s = pickle.load(open(path,'rb'))
			return ppr_s[t]
		else:
			raise NameError('No path found for ' + path)

	def ppr_vec(self,s,alpha):

		ppr_dir = self.PATH['ppr']
		name = s + '-' + str(alpha) + '.pkl'
		path = os.path.join(ppr_dir,name)

		if os.path.exists(path):
			return pickle.load(open(path,'rb'))
		else:
			raise NameError('No path found for ' + path)



