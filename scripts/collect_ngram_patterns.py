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
            - debug flag                     :: Bool
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
            output.write(gram + '\t' + n + '\n')

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

            - refresh flag                   :: Bool

                 if true then do not rerun if file exits

            - debug flag                     :: Bool
                 if true only output part of ngrams
    @Output: None
            save results of parse to out_path
            log program trace to log_dir
'''
def collect_ngram_patterns( word_path
                          , pattern_path
                          , ngram_dir
                          , out_dir
                          , log_dir
                          , refresh = True
                          , debug   = False):
    
    # log output
    writer = Writer(log_dir, 1, debug)

    '''
        path to word_path-no-data.txt
        - this is created the last time we crawled and found no data
    '''
    no_data_path = os.path.splitext(word_path)[0] + '-no-data' + '.txt'

    '''
        if we crawled this set of words before, then we
        encountered words with no data and saved them.
        so open them up
    '''
    if os.path.exists(no_data_path):

        tup = lambda xs : (xs[0], xs[1])

        writer.tell('found path to list of pairs with no data at ' + no_data_path)
        no_data_pairs = [tup(x.split(', ')) for x in open(no_data_path,'rb').read().split('\n') if x]

    else:
        writer.tell('could not locate list of pairs with no data at ' + no_data_path)
        no_data_pairs = []

    s_refresh = 'refresh' if refresh else 'non-refresh'
    patterns  = read_pattern(pattern_path)
    pairs     = [x.split(', ') for x in open(word_path,'rb').read().split('\n') if x]

    writer.tell('running collect_ngram_patterns ...')
    writer.tell('found word pair path at ' + word_path)
    writer.tell('found ngram directory at ' + ngram_dir)
    writer.tell('collect ngram over all words in ' + s_refresh + ' mode...')

    '''
        loop over pairs so we can save as data for each pair is collected
        re-save the no_data_pairs to disk for every new k pairs added
    '''
    save_curr = 0

    for s,t in pairs:

        s_t_path = os.path.join(out_dir, s + '-' + t + '.txt')

        if (s,t) in no_data_pairs:

            writer.tell(s + ', ' + t + ' did not have data the last time we crawled. skipping ...')

        elif refresh and os.path.exists(s_t_path):
            writer.tell('data for ' + s + ', ' + t + ' already exists. skipping ...')

        else:
    
            found = go_collect(s, t, patterns, ngram_dir, s_t_path, debug)

            if not found: 
                no_data_pairs.append((s,t))
                save_curr += 1

        '''
            update no-data-pairs on disk
        '''
        if save_curr == 5: 
            writer.tell('saving partial results for no-data-pairs')
            save_no_data_pairs(no_data_pairs, no_data_path)
            save_curr = 0


    writer.tell('saving list of words with no data at ' + no_data_path)

    if no_data_pairs:
        with open(no_data_path,'wb') as h:
            for s,t in set(no_data_pairs):
                h.write(s + ', ' + t + '\n')

    writer.close()          

def save_no_data_pairs(pairs, path):
    if pairs:
        with open(path, 'wb') as h:
            for s, t in set(pairs):
                h.write(s + ', ' + t + '\n')


'''
    @Use: collect data for words s,t over all `patterns`
          from ngrams found at `ngram_dir`
          save output to `s_t_path`
          and respect `debug` flag
'''
def go_collect(s, t, patterns, ngram_dir, s_t_path, debug):

    out   = {s + '>' + t : [], s + '<' + t : []}
    patts = compile_patterns(s,t,patterns)

    for gram,n in with_ngram(ngram_dir, debug):

        if s in gram and t in gram:

            s_stronger_t = [gram + '\t' + n for r in patts[s + '>' + t] if r.match(gram)]
            s_weaker_t   = [gram + '\t' + n for r in patts[s + '<' + t] if r.match(gram)]

            out[s + '>' + t] += s_stronger_t             
            out[s + '<' + t] += s_weaker_t
    
    if out[s + '>' + t] or out[s + '<' + t]:

        with open(s_t_path, 'wb') as h:

            h.write('=== ' + s + ' > ' + t  + '\n')

            for p in out[s + '>' + t]: h.write(p + '\n')

            h.write('\n=== ' + s + ' < ' + t  + '\n')

            for q in out[s + '<' + t]: h.write(q + '\n')

            h.write('=== END')       

        return True
    else:

        return False



'''
    @Use  : compile word pattern for every pattern
    @Input: s     :: String  word1
            t     :: String  word2
            patts :: Dict String [String]
                      with keys: strong-weak
                                 weak-strong
                      and values that is a list of patterns
    @Output a dictionary of regular expressions for 
            s t at each pattern
'''
def compile_patterns(s,t, patts):

    s_stronger_t = [re.compile(parse_re(R,[s,t])) for R in patts['strong-weak']] \
                 + [re.compile(parse_re(R,[t,s])) for R in patts['weak-strong']]

    s_weaker_t  = [re.compile(parse_re(R,[s,t])) for R in patts['weak-strong']]  \
                + [re.compile(parse_re(R,[t,s])) for R in patts['strong-weak']]

    return { s + '>' + t : s_stronger_t, s + '<' + t : s_weaker_t }





'''
    @depricated: stream over ngram once

    iterate over all ngrams and parse all permutations of s R t
    for words s,t and patterns R
    for gram,n in with_ngram(ngram_dir, debug):

    # pair_patterns = [(s,t,compile_patterns(s,t,patterns)) \
                 # for s,t in pairs]          

# results   = { (s,t) : {s + '>' + t : [], s + '<' + t : []} for s,t in pairs }

writer.tell( 'Streaming ngrams from ' + ngram_dir )



    for s,t, st_patterns in pair_patterns:

        if s in gram and t in gram:
                        collect patterns and save
    
            s_stronger_t = [gram + '\t' + n for r in st_patterns[s + '>' + t] if r.match(gram)]
            s_weaker_t   = [gram + '\t' + n for r in st_patterns[s + '<' + t] if r.match(gram)]

            results[(s,t)][s + '>' + t] += s_stronger_t             
            results[(s,t)][s + '<' + t] += s_weaker_t


    save outputs for each s-t pairs
    if there are any pattern matches

writer.tell('saving all results ...')

for (s,t),res in results.iteritems():

    if res[s + '>' + t] or res[s + '<' + t]:

        writer.tell('found patterns for word pair ' + s + ' and ' + t)

        with open(os.path.join(out_dir, s + '-' + t + '.txt'), 'wb') as h:

            h.write('=== ' + s + ' > ' + t  + '\n')

            for p in res[s + '>' + t]: h.write(p + '\n')

            h.write('\n=== ' + s + ' < ' + t  + '\n')

            for q in res[s + '<' + t]: h.write(q + '\n')

            h.write('=== END')          
'''



