from dbm import column_base
import StringIO
import types;

######## Test Functions Begin ##########
class TestItem:
	pass

def __test_sel(o):
	return True

def __test_sel2(o):
	return isinstance(o, types.StringTypes)

def __test_sel3(o):
	return isinstance(o, types.TupleType)

def __test_select(c, r):
	print "############# select with column value round:", r
	print "round:%d-1" % r
	for item in c.select_with_column_value(("col1", "tt2")):
		print "[", item.col1, item.col2, item.col3, "]"
	print "round:%d-2" % r
	for item in c.select_with_column_value(("col2", "tt2")):
		print "[", item.col1, item.col2, item.col3, "]"
	print "round:%d-3" % r
	for item in c.select_with_column_value(("col2", 1)):
		print "[", item.col1, item.col2, item.col3, "]"
	print "round:%d-4" % r
	for item in c.select_with_column_value(__test_sel):
		print "[", item.col1, item.col2, item.col3, "]"
	print "round:%d-5" % r
	for item in c.select_with_column_value(__test_sel2):
		print "[", item.col1, item.col2, item.col3, "]"
	print "round:%d-6" % r
	for item in c.select_with_column_value(__test_sel3):
		print "[", item.col1, item.col2, item.col3, "]"
	print "round:%d-7" % r
	for item in c.select_with_column(__test_sel2):
		print "[", item.col1, item.col2, item.col3, "]"
	print "round:%d-8" % r
	for item in c.select_with_column("col1"):
		print "[", item.col1, item.col2, item.col3, "]"
	print "round:%d-9" % r
	for item in c.select_with_column("col2"):
		print "[", item.col1, item.col2, item.col3, "]"
	print "round:%d-10" % r
	for item in c.select_with_column("col20"):
		print "[", item.col1, item.col2, item.col3, "]"
	print "round:%d-11" % r
	for item in c.select_with_column(__test_sel):
		print "[", item.col1, item.col2, item.col3, "]"
	print "round:%d-12" % r
	for item in c.select_with_column(__test_sel2):
		print "[", item.col1, item.col2, item.col3, "]"
	print "round:%d-13" % r
	for item in c.select_with_column(__test_sel3):
		print "[", item.col1, item.col2, item.col3, "]"

def __test_func():
	c = column_base.ColumnBase()
	print c.select_with_column.__doc__

	mm = {}
	mm["abc"] = [1,2,3,4,5, c]
	mm["def"] = [6,7,8,9,0,2,4,5]

	ss = set()

	ss |= set(mm["abc"])
	ss |= set(mm["def"])
	ss |= set('abcd')

	print [v for v in ss]

	vv = ('acb',1000)

	print vv[0], vv[1]

	tt = TestItem()
	tt.col1 = "col1"
	tt.col2 = 1
	tt.col3 = True
	c.insert(tt)

	tt = TestItem()
	tt.col1 = "tt2"
	tt.col2 = 1000
	tt.col3 = False
	c.insert(tt)

	ssii = StringIO.StringIO()

	c.save_to(ssii)

	#print ssii.getvalue()

	print "#####################\n"
	cc = column_base.ColumnBase()
	cc.load_from(StringIO.StringIO(ssii.getvalue()))

	ssiiii = StringIO.StringIO()
	cc.save_to(ssiiii)

	#print ssiiii.getvalue()

	print "##############\n"

	for item in cc.items():
		print item.col1, item.col2, item.col3

	print "##############\n"
	for item in c.items():
		print item.col1, item.col2, item.col3

	print "############# select with column\n"
	for item in c.select_with_column("col1"):
		print item.col1, item.col2, item.col3

	__test_select(c, 1)
	print "delete 0:", c.delete_with_column_value(("col1", "tt2"))
	__test_select(c, 2)
	print "delete 1:", c.delete_with_column("col1")
	__test_select(c, 3)

class TestDescriptor(object):
	def __init__(self, col, val):
		self.val = val
		self.col = col

	def __get__(self, obj, objtype = None): 
		print "+++++get attribute for:", self.col, self.val
		return self.val

	def __set__(self, obj, val): 
		self.val = val
		print "-----set attribute for:", self.col, self.val

	def __delete__(self, obj):
		print "*****del attribute for:", self.col, self.val

class TestObject(object):
	x = TestDescriptor("x", "123")
	y = 789

def __test_descriptor():
	v = TestItem()
	v.x = TestDescriptor("x", "123")
	print v.x
	v.x = "789"
	print v.x
	delattr(v, "x")

	vv = TestObject()
	print vv.x
	print vv.y

	vv.x = "567"
	print vv.x

	delattr(vv, "x")

	print hasattr(vv,"x")
	print vv.x

######### Test Functions End ############

def do_test():
	__test_func()
	__test_descriptor()

if __name__ == "__main__":	
	do_test()

