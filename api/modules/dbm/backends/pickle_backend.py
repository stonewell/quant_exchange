# System includes
import os
import sys
import types
import cPickle
import pickle
from .. import column_base_backend

class PickleBackend(column_base_backend.ColumnBaseBackend):
	def save_to(self, obj, filename):
		if isinstance(filename, types.StringTypes):
			cPickle.dump(obj, open(filename, "wb"))
		else:
			cPickle.dump(obj, filename)

	def load_from(self, obj, filename):
		if isinstance(filename, types.StringTypes):
			cPickle.load(open(filename, "rb"))
		else:
			cb = cPickle.load(filename)

		obj.clear()

		for item in cb.items():
			obj.insert(item)

		cb.clear()


