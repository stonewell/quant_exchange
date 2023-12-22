# System includes
import os
import sys
import types
import StringIO
import column_base_backend
import default_backend
import utils.list_utils

class ColumnBase:
	def __init__(self, backend = default_backend.default_backend()):
		self.backend = backend

		self.clear()

	def insert(self, item):
		if item in self.__item_to_props:
			return False

		cols = self.__get_item_columns(item)

		if len(cols) == 0:
			return False

		props = {}
		self.__item_to_props[item] = props

		for col in cols:
			val = self.__get_item_column_value(item, col)
			self.__on_column_changed(item, col, None, val)

		return True

	def update(self, item):
		self.delete(item)
		self.insert(item)

	def delete(self, item):
		if item not in self.__item_to_props:
			return False

		cols = self.__get_item_columns(item)

		for col in cols:
			val = self.__get_item_column_value(item, col)
			self.__on_column_changed(item, col, val, None)

		props = self.__item_to_props.pop(item, None)

		#Check if other columns/value still reference item
		if props != None:
			for col in iter(props):
				self.__on_column_changed(item, col, props[col], None)

		return True

	def clear(self):
		self.__item_to_props = self.backend.create_dict()
		self.__col_to_items = self.backend.create_dict()
		self.__val_to_items = self.backend.create_dict()
		self.__col_to_vals = self.backend.create_dict()

	def items(self):
		return self.__item_to_props.keys();

	def delete_with_column(self, sel):
		for item in self.select_with_column(sel):
			self.delete(item)

		return True
	
	def delete_with_column_value(self, sel):
		for item in self.select_with_column_value(sel):
			self.delete(item)
		
		return True

	def __get_item_columns(self, item):
		"""
		Find supported columns in item's attributes
		Only simple type supported: None, Boolean, Int, Long, Float, String, Unicode
		"""
		cols = []

		for col in dir(item):
			v = getattr(item, col)
			if ((isinstance(v, types.NoneType) or
				isinstance(v, types.BooleanType) or
				isinstance(v, types.IntType) or
				isinstance(v, types.LongType) or
				isinstance(v, types.FloatType) or
				isinstance(v, types.StringTypes)) and
				cmp(col, "__doc__") != 0 and
				cmp(col, "__module__") != 0):
				cols.append(col)

		return cols

	def __get_item_column_value(self, item, col):
		if hasattr(item, col):
			return getattr(item, col)

		return None

	def select_with_column(self, sel):
		"""
		When sel is an callable object and accept single string argument, 
		column base will call it to determin which column to be included in operation.
		When sel is not callable, it will use as column name to make exactly matching
		"""
		if not hasattr(self, "_%s__col_to_items" % self.__class__.__name__):
			return []

		if isinstance(sel, types.StringTypes):
			return self.__col_to_items.get(sel, [])

		results_set = set()

		for col in iter(self.__col_to_items):
			if sel(col):
				results_set |= set(self.__col_to_items[col])

		return [v for v in results_set]

	def select_with_column_value(self, sel):
		"""
		When sel is an callable object and accept a turple argument, 
		column base will call it to determin which (column,value) turple to be included in operation.
		When sel is not callable, it will use as (column,value) turple to make exactly matching
		"""
		if not hasattr(self, "_%s__col_to_vals" % self.__class__.__name__):
			return []
		
		if isinstance(sel, types.TupleType):
			if not sel[0] in self.__col_to_vals:
				return []

			if not column_base_utils.contains(self.__col_to_vals[sel[0]], sel[1]):
				return []

			col_items = self.__col_to_items.get(sel[0], [])
			val_items = self.__val_to_items.get(sel[1], [])

			return [v for v in set(col_items) & set(val_items)]

		results_set = set()

		for col in iter(self.__col_to_vals):
			vals = self.__col_to_vals[col]

			for val in vals:
				if sel((col,val)):
					col_items = self.__col_to_items.get(col, [])
					val_items = self.__val_to_items.get(val, [])

					results_set |= (set(col_items) & set(val_items))

		return [v for v in results_set]

	def select_with_value(self, sel):
		"""
		When sel is an callable object and accept single argument,
		column base will call it to determin which value to be included in operation.
		When sel is not callable, it will use as value to make exactly matching
		"""
		if not hasattr(self, "_%s__val_to_items" % self.__class__.__name__):
			return []

		if sel in self._val_to_items:
			return self.__val_to_items.get(sel, [])

		results_set = set()

		for val in iter(self.__val_to_items):
			if sel(val):
				results_set |= set(self.__val_to_items[val])

		return [v for v in results_set]
		
	def save_to(self, filename):
		self.backend.save_to(self, filename)

	def load_from(self, filename):
		self.backend.load_from(self, filename)

	def __on_column_changed(self, obj, col, old_val, new_val):
		if obj not in self.__item_to_props:
			return

		# update item properties mapping
		props = self.__item_to_props[obj]

		if new_val == None:
			props.pop(col, None)
		else:
			props[col] = new_val

		# check column to item mapping
		if col in self.__col_to_items:
			l = self.__col_to_items[col]

			if new_val != None:
				if not column_base_utils.contains(l, obj):
					l.append(obj)
			else:
				utils.list_utils.del_noerr(l, obj)

				if len(l) == 0:
					self.__col_to_items.pop(col, None)					
		elif new_val != None:
			l = [obj]
			self.__col_to_items[col] = l

		if old_val != new_val and old_val != None:
			#Need remove all reference_to old value
			if old_val in self.__val_to_items:
				l = self.__val_to_items[old_val]
				utils.list_utils.del_noerr(l, obj)
			if col in self.__col_to_vals:
				l = self.__col_to_vals[col]
				utils.list_utils.del_noerr(l, old_val)
		
		if new_val != None:
			if new_val in self.__val_to_items:
				l = self.__val_to_items[new_val]
				if not utils.list_utils.contains(l, obj):
					l.append(obj)
			else:
				l = [obj]
				self.__val_to_items[new_val] = l
			
			if col in self.__col_to_vals:
				l = self.__col_to_vals[col]
				if not utils.list_utils.contains(l, new_val):
					l.append(new_val)
			else:
				l = [new_val]
				self.__col_to_vals[col] = l
