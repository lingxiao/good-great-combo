############################################################
# Module  : collect ngrams matching linguistic patterns
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
import re

from utils   import *
from scripts import *


'''
	@Use  : find all ngrams matching "word_a pattern word_b" regex
	@Input: - path to words  `word_path`     :: String
	        - path to pattern `pattern_path` :: String
	        - path to ngrams  `ngram_dir`    :: String
	        - output directory `out_dir`     :: String
	        - log path `log_dir`             :: String 
	@Output: None
			save results of parse to out_path
			log program trace to log_dir
'''
def collect_ngram_patterns(word_path, pattern_path, ngram_dir, out_dir, log_dir):

	writer = Writer(log_dir, 1)
	writer.tell('running collect_ngram_patterns ...')

	patterns  = read_pattern(pattern_path)
	pairs     = [x.split(', ') for x in open(word_path,'rb').read().split('\n') if x]

	results   = {(s,t) : {'weak-strong' : [], 'strong-weak': []} for s,t in pairs}           

	writer.tell('found word pair path at ' + word_path)

	'''
		iterate over all ngrams and parse all permutations of s R t
		for words s,t and patterns R
	'''
	for gram,n in with_ngram(ngram_dir):

		for s,t in pairs:

			for R in patterns['strong-weak']:

				reg = re.compile(parse_re(R,[s,t]))

				if reg.match(gram):
					results[(s,t)]['strong-weak'].append((gram,n))

			for R in patterns['weak-strong']:

				reg = re.compile(parse_re(R,[t,s]))

				if reg.match(gram):
					results[(s,t)]['strong-weak'].append((gram,n))

			for R in patterns['weak-strong']:

				reg = re.compile(parse_re(R,[s,t]))
				if reg.match(gram):
					results[(s,t)]['weak-strong'].append((gram,n))

			for R in patterns['strong-weak']:

				reg = re.compile(parse_re(R,[t,s]))
				if reg.match(gram):
					results[(s,t)]['weak-strong'].append((gram,n))


	'''
		save outputs for each s-t pairs
	'''
	for (s,t),res in pairs.iteritems():

		if res['strong-weak'] or res['weak-strong']:

			with open(os.path.join(out_dir, s + t + '.txt'), 'wb') as h:
				h.write('=== strong-weak\n')

				for p in res['strong-weak']:
					h.write(p + '\n')

				h.write('=== weak-strong\n')

				for q in res['weak-strong\n']:
					h.write(q + '\n')

				h.write('=== END')


	writer.close()			


	# if not os.path.exists(word_path):
	# 	raise NameError('File not found at ' + word_path)

	# else:

		# writer.tell('found word pair path at ' + word_path)
		# patterns  = read_pattern(pattern_path)
		# patts     = patterns['strong-weak'] + patterns['weak-strong']
		# regexes   = [re.compile(parse_re(r, [s,t])) for r in patts for s,t in pairs]

		# writer.tell('collecting patterns over ' + str(len(regexes)) + ' regular expressions')

		# pairs     = [x.split(', ') for x in \
		#             open(word_path,'rb').read().split('\n') if x]

		# pairs = {s + '-' + t : {'weak-strong' : [], 'strong-weak'} for s,t in pairs}           

		# print(pairs)



	# out = open(out_path,'wb')	

	# for xs,n in with_ngram(ngram_dir):
	# 	for reg in regexes:
	# 		if reg.match(xs): 
	# 			out.write(xs + ': ' + n + '\n')

	# out.write('=== END')	
	# out.close()

	# writer.tell('saving file at ' + out_path)
	# writer.close()

