############################################################
# Unit test
############################################################


import pytest

############################################################
# Main
############################################################

def main():
	t_dot ()
	t_add ()
	t_sub ()
	t_mult()
	t_sign()
	t_sign_esp()

	t_init ()
	t_embed()
	t_label()

############################################################
# label algebra


def t_rank_by_majority():

	u1 = [1,0,0]
	u2 = [0,1,0]
	u3 = [0,0,1]

	assert rank_by_majority(LABEL,'u','v', u1,u1  ) == [('u','v'),('v','u')]
	assert rank_by_majority(LABEL,'u1','u2', u1,u2) == [('u2','u1')]
	assert rank_by_majority(LABEL,'u1','u3', u1,u3) == [('u1','u3')]
	assert rank_by_majority(LABEL,'u2','u3', u2,u3) == [('u2','u3')]

	u4 = [0,0.65,0.35]
	u5 = [0,0.60,0.40]

	u6 = [0,0.35,0.65]
	u7 = [0,0.40,0.60]


	assert rank_by_majority(LABEL,'u4','u5', u4,u5) == [('u4','u5')]
	assert rank_by_majority(LABEL,'u6','u7', u6,u7) == [('u7','u6')]

	assert rank_by_majority(LABEL,'u6','u7', u6,u7) == rank_by_majority(LABEL,'u7','u6',u7,u6)

	print 'passed rank by majority'




def t_label_gt(LABEL):
	d = LABEL[-1]
	i = LABEL[1]
	n = LABEL[0]

	assert label_gt(LABEL,n,n) == False
	assert label_gt(LABEL,n,i) == True
	assert label_gt(LABEL,n,d) == False
	assert label_gt(LABEL,i,n) == False
	assert label_gt(LABEL,i,d) == False
	assert label_gt(LABEL,i,i) == False
	assert label_gt(LABEL,d,d) == False
	assert label_gt(LABEL,d,n) == True
	assert label_gt(LABEL,d,i) == True

	assert label_lt(LABEL,n,n) == False
	assert label_lt(LABEL,n,i) == (not True)
	assert label_lt(LABEL,n,d) == (not False)
	assert label_lt(LABEL,i,n) == (not False)
	assert label_lt(LABEL,i,d) == (not False)
	assert label_lt(LABEL,i,i) == False
	assert label_lt(LABEL,d,d) == False
	assert label_lt(LABEL,d,n) == (not True)
	assert label_lt(LABEL,d,i) == (not True)

	print 'passed label order'


############################################################
# initalization

def t_init():
	train = {('1','2'): {'1': ['a','b'], '2': ['c','d']} \
	        ,('1','4'): {'1': ['e','f'], '4': ['a','b']} }

	assert init(train) == {'a':0.0,'b':0.0,'c':0.0,'d':0.0,'e':0.0,'f':0.0}
	print 'pased init'

def t_embed():
	basis = {'foo': 0.0, 'bar': 0.0}
	data  = {'strong': ['foo'] }
	assert embed(basis,data['strong']) == {'foo': 1.0, 'bar': 0}
	print "passed embed"

def t_label():
	d1 = {'rank': 'a > b'}
	d2 = {'rank': 'a < b'}
	d3 = {'rank': 'a = b'}
	assert label(d1) == 1.0
	assert label(d2) == -1.0
	assert label(d3) == 0.0
	print "passed label"


############################################################
# vector primitives

def t_sign_esp():
	eps = 1e-3
	assert sign_eps(0.9 ,eps)  ==  1
	assert sign_eps(-0.9,eps)  == -1
	assert sign_eps(1e-4,eps)  ==  0
	assert sign_eps(-1e-4,eps) ==  0
	print 'passed sign_eps'

def t_dot():
	x = {'x': 1, 'y': 2 , 'z': 3}
	y = {'x': 4, 'y': -5, 'z': 6}
	z = {'x': 0, 'y': 0, 'z': 0}

	# vector algebra
	assert dot(x,y)  == dot(y,x)       # commutative
	assert dot(x,z)  == 0.0            # right id
	assert dot(z,x)  == 0.0            # left id

	# correct
	assert dot(x,y)  == 12.0
	assert dot({'x': -4, 'y': -9}, {'x': -1, 'y': 2}) == -14
	print "passed dot product"

def t_add():
	x = {'x': 1, 'y': 2 , 'z': 3}
	y = {'x': 4, 'y': -5, 'z': 6}
	z = {'x': 0, 'y': 0, 'z': 0}
	u = {'x': 10, 'y': 5, 'z': 2}


	# vector algebra
	assert add(x,y) == add(y,x)                # commutatitive
	assert add(z,y) == y                       # right id
	assert add(y,z) == y                       # left id
	assert add(x, add(y,u)) == add(add(x,y),u) # associative

	# correct
	assert add(x,y)	== {'x': 5, "y": -3, 'z': 9}


	print "passed vector addition"

def t_mult():
	x = {'x': 1.0, 'y': 2.0, 'z': 3.0}
	y = {'x': 10, 'y': 20, 'z': 30}

	v = mult(x,20)

	assert mult(x,1 ) == x
	assert mult(x,0 ) == {'x': 0, 'y': 0, 'z': 0}
	assert mult(x,10) == y
	assert          x != v
	print "passed vector scaling"

def t_sub():
	x = {'x': 1.0, 'y': 2.0, 'z': 3.0}
	y = {'x': 10, 'y': 20, 'z': 30}

	assert sub(x,x) == {'x':0,'y':0,'z':0}
	assert sub(x,y) == {'x':-9,'y': -18, 'z': -27}
	print 'passed vector subtraction'

def t_sign():
	return sign(-3) == False
	return sign(30) == True
	return sign(0)  == False
	print "passed sign"

