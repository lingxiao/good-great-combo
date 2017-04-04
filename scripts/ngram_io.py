############################################################
# Module  : Open Ngram and read linguistic pattern
# Date    : April 3rd, 2017
# Author  : Xiao Ling, merle
############################################################

import os


############################################################
'''
	@Use   : Open all ngrams in ngram_dir and stream output as tuple of (ngram, count)
	@Input : - ngram_dir :: String
	         - debug     :: Bool,  if true then only output parts of stream
	@Output: Iterator output ngrams of form:
				(ngram, count) :: Iterator (String, String)

			Throw: NameError if path does not exists
'''
def with_ngram(ngram_dir, debug = False):

	if not os.path.exists(ngram_dir):
		raise NameError('Path not found at ' + ngram_dir)

	else:

		ngram_paths = [os.path.join(ngram_dir, p) for \
		               p in os.listdir(ngram_dir) if '.txt' in p]	

		if not ngram_paths:
			raise NameError('Directory Empty at ' + ngram_dir)

		if debug:
			ngram_paths = [ngram_paths[0]]		              

		for path in ngram_paths:

			with open(path, 'rb') as h:
				for line in h:
					xsn = line.split('\t')
					if len(xsn) == 2:
						xs,n = xsn
						n,_  = n.split('\n')
						yield (xs,n)

############################################################
'''
	@Use: Given path to linguistic pattern, output pattern
'''
def read_pattern(pattern_path):

	if os.path.exists(pattern_path):

		strong_weak, weak_strong  = open(pattern_path,'rb').read().split('=== weak-strong')
		strong_weak = [p for p in strong_weak.split('\n') if p][1:]
		weak_strong = [p for p in weak_strong.split('\n') if p][:-1]

		return {'strong-weak': strong_weak, 'weak-strong': weak_strong}

	else:
		raise NameError('Cannot find pattern at path ' + pattern_path)
