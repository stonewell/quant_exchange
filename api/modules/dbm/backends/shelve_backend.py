# System includes
import os
import sys
import types
import column_base_backend
import shelve

class ShelveBackend(column_base_backend.ColumnBaseBackend):
	def save_to(self, obj, filename):
		store = shelve.open(filename)
		store["items"] = self.__item_to_index 
		store.close()

	def load_from(self, obj, filename):
		obj.clear()

		store = shelve.open(filename)

		for item in store["items"]:
			obj.insert(item)
