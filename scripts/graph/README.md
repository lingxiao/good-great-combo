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

