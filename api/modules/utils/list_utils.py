def index_noerr(l, v):
	try:
		return l.index(v)
	except ValueError:
		return -1

def contains(l, v):
	return index_noerr(l,v) >= 0

def del_noerr(l, v):
	index = index_noerr(l, v)
	if index >= 0:
		del l[index]
		
