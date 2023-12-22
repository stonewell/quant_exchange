import sys
import struct
import os

from . import day_data
from . import five_minute_data

day_data_rec_fmt = '<iiiiifii'
day_data_rec_size = struct.calcsize(day_data_rec_fmt)

five_min_data_rec_fmt = '<hhfffffff'
five_min_data_rec_size = struct.calcsize(five_min_data_rec_fmt)

def create_day_data(val_array):
	data = day_data.DayData()
	data.date = val_array[0]
	data.open_price = float(val_array[1])
	data.highest_price = float(val_array[2])
	data.lowest_price = float(val_array[3])
	data.close_price = float(val_array[4])
	data.amount = float(val_array[5])
	data.vol = float(val_array[6])
	data.reserved = val_array[7]

	return data

def create_five_min_data(val_array):
	data = five_minute_data.FiveMinuteData()
	data.date = val_array[0]
	data.time = val_array[1]
	data.buy_lowest = float(val_array[2])
	data.buy_highest = float(val_array[3])
	data.sell_lowest = float(val_array[4])
	data.sell_highest = float(val_array[5])
	data.amount = float(val_array[6])
	data.reserved1 = val_array[7]
	data.reserved2 = val_array[8]

	return data

def __file_size(f):
	saved_pos = f.tell()
	f.seek(0, os.SEEK_END)

	filesize = f.tell()
	f.seek(saved_pos, os.SEEK_SET)
	return filesize

def __read_all_data(f, fmt, rec_size, data_create_func):
	saved_pos = f.tell()
	f.seek(0, os.SEEK_SET)

	s = f.read(rec_size)

	all_data = []

	while len(s) == day_data_rec_size:
		all_data.append(data_create_func(struct.unpack(fmt, s)))
		s = f.read(rec_size)

	f.seek(saved_pos, os.SEEK_SET)

	return all_data

def __read_next(f, fmt, rec_size, data_create_func, rec_offset = 0, offset_dir = os.SEEK_CUR):
	f.seek(rec_offset * rec_size, offset_dir)

	data = None

	s = f.read(rec_size)

	if len(s) == rec_size:
		data = data_create_func(struct.unpack(fmt, s))

	return data

def read_all_day_data(f):
	return __read_all_data(f, day_data_rec_fmt, day_data_rec_size, create_day_data)

def read_next_day_data(f, rec_offset = 0, offset_dir = os.SEEK_CUR):
	return __read_next(f, day_data_rec_fmt, day_data_rec_size, create_day_data, rec_offset, offset_dir)

def read_all_five_min_data(f):
	return __read_all_data(f, five_min_data_rec_fmt, five_min_data_rec_size, create_five_min_data)

def read_next_five_min_data(f, rec_offset = 0, offset_dir = os.SEEK_CUR):
	return __read_next(f, five_min_data_rec_fmt, five_min_data_rec_size,
					   create_five_min_data, rec_offset, offset_dir)
