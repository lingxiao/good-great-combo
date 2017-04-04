############################################################
# Module  : Translate paper's parser pattern syntax 
#           to regular expression
# Date    : November 6th, 2016
# Author  : Xiao Ling
############################################################

import re
import string

############################################################
# Parse paper's regexp to python regexp
############################################################

# @Input : String defining linguistic pattern in paper's syntax
#          list of words to fill in the holes of regex
#          if list empty, then output regex matching any string
#          where the hole is found
# @Output: Python regular expression
# parse_re :: String -> [String] -> String
def parse_re(rs,words): 
	return go(rs.split(),words)

############################################################
# converting twosided patterns to onesided 
############################################################

def fill_fst(p):
  return ' '.join(fill(p.split(' ')))

def fill_snd(p):
  p = p.split(' ')
  p.reverse()
  ws = fill(p)
  ws.reverse()
  return ' '.join(ws)

def fill(ws):
  i  = ws.index('*')
  ws[i] = '<*>'
  return ws	

############################################################
# Helpers 

def go(rss,words):
	if not rss: return ""
	else:
		head = rss[0 ]
		tail = rss[1:]

		# translate token to regular expression
		if words: token = parse_each(head,words[0])
		else    : token = parse_each(head,r'.+'   )

		# add space if needed
		if tail and not optional(tail[0]): token += "\s+"

		# recurse
		if hole(head): return token + go(tail,words[1:])
		else         : return token + go(tail,words    )


def parse_each(rs,ai):
	if wild(rs):
		return r'.+\b'
	elif hole(rs):
		return ai + r'\b'
	elif optional(rs):
		return option(rs[1:len(rs)-1])
	else:
		return rs + r'\b'

def option(rs):
	out = "("
	rss = rs.split("|")
	for rs in rss:
		if rs in string.punctuation:
			out += "\s*" + rs + "|"
		else: 
			out += "\s+" + rs + "|"
	return out[:len(out)-1] + ")?"

############################################################
# predicates

# @Use : if '<*>' appears in pattern then
#        replace it with '.+'
def wild(rs):
	return rs == '<*>'

# @Use : if '*' appears in pattern then
#        replace it with a word if possible,
#        else replace with '.+'
def hole(rs): return rs == "*"

def optional(rs):
	return rs[0] == "(" and rs[-1] == ")"

