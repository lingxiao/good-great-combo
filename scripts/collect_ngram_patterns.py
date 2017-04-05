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
	@Use: winnow ngram files by those that contain words found in word_path
	      Note if you run this on multiple batchs of words from different `word_path`
	      then there will be duplicate ngrams

	      then you would need to prune the output files for duplicates

	@Input: - path to words  `word_path`     :: String
	        - path to ngrams  `ngram_dir`    :: String
	        - output directory `out_dir`     :: String
	        - log path `log_dir`             :: String 
	        - debug flag  	                 :: Bool
	             if true only output part of ngrams
	@Output: None
			save results of parse to out_path
			log program trace to log_dir
'''
def ngram_by_words(word_path, ngram_dir, out_path, log_dir, debug = False):

	writer = Writer(log_dir, 1)
	writer.tell('running ngram_by_words ...')

	if debug: msg = 'debug'
	else:     msg = 'non-debug'
	writer.tell('Streaming ngrams from ' + ngram_dir +  ' in ' + msg + ' mode')

	words   = [x for x in open(word_path, 'rb').read().split('\n') if x]

	output  = open(out_path, 'wb')

	'''
		iterate over all ngrams and save if any word in words appear
	'''
	for gram,n in with_ngram(ngram_dir, debug):
		if any(w in gram for w in words):
			output.write(gram + ': ' + n + '\n')

	output.write('=== END')
	output.close()
	writer.close()



'''
	@Use  : find all ngrams matching "word_a pattern word_b" regex
	@Input: - path to words  `word_path`     :: String
	        - path to pattern `pattern_path` :: String
	        - path to ngrams  `ngram_dir`    :: String
	        - output directory `out_dir`     :: String
	        - log path `log_dir`             :: String 
	        - debug flag  	                 :: Bool
	             if true only output part of ngrams
	@Output: None
			save results of parse to out_path
			log program trace to log_dir
'''
def collect_ngram_patterns(word_path, pattern_path, ngram_dir, out_dir, log_dir, debug = False):

	writer = Writer(log_dir, 1)
	writer.tell('running collect_ngram_patterns ...')

	patterns  = read_pattern(pattern_path)
	pairs     = [x.split(', ') for x in open(word_path,'rb').read().split('\n') if x]

	results   = {(s,t) : {'weak-strong' : [], 'strong-weak': []} for s,t in pairs}           

	writer.tell('found word pair path at ' + word_path)

	if debug: msg = 'debug'
	else:     msg = 'non-debug'
	writer.tell('Streaming ngrams from ' + ngram_dir +  ' in ' + msg + ' mode')


	'''
		iterate over all ngrams and parse all permutations of s R t
		for words s,t and patterns R
	'''
	for gram,n in with_ngram(ngram_dir, debug):

		for s,t in pairs:

			'''
				collect patterns and save
			'''
			for R in patterns['strong-weak']:

				reg = re.compile(parse_re(R,[s,t]))

				if reg.match(gram):
					results[(s,t)]['strong-weak'].append(gram + ': ' + n)

			for R in patterns['weak-strong']:

				reg = re.compile(parse_re(R,[t,s]))

				if reg.match(gram):
					results[(s,t)]['strong-weak'].append(gram + ': ' + n)

			for R in patterns['weak-strong']:

				reg = re.compile(parse_re(R,[s,t]))
				if reg.match(gram):
					results[(s,t)]['weak-strong'].append(gram + ': ' + n)

			for R in patterns['strong-weak']:

				reg = re.compile(parse_re(R,[t,s]))
				if reg.match(gram):
					results[(s,t)]['weak-strong'].append(gram + ': ' + n)

	'''
		save outputs for each s-t pairs
		if there are any pattern matches
	'''
	for (s,t),res in results.iteritems():

		if res['strong-weak'] or res['weak-strong']:

			writer.tell('found patterns for word pair ' + s + ' and ' + t)

			with open(os.path.join(out_dir, s + '-' + t + '.txt'), 'wb') as h:

				h.write('=== strong-weak\n')

				for p in res['strong-weak']:
					h.write(p + '\n')

				h.write('=== weak-strong\n')

				for q in res['weak-strong']:
					h.write(q + '\n')

				h.write('=== END')			



	writer.close()			


