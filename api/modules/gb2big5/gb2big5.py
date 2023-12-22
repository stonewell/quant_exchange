# coding=UTF-8
import chardet
import os
import StringIO
import gb2big5_table
import gb2big5_table_1
import gb2big5_table_2

class GB2Big5:
	def __init__(self):
		self.gb2big5_mapping = {}
		self.big52gb_mapping = {}

	def convert(self, in_file, out_file, to_big5 = True):
		#detect encoding
		f_pos = in_file.tell()
		f_sample = in_file.read(5000)
		encoder = chardet.detect(f_sample)
		in_file.seek(f_pos, os.SEEK_SET)

		conv_mapping = self.get_conv_mapping(to_big5)

		for line in in_file:
			line1 = unicode(line, encoder['encoding'])
			out_line = StringIO.StringIO()
			for c in line1:
				if c in conv_mapping:
					out_line.write(conv_mapping[c])
				else:
					out_line.write(c)
			out_file.writelines(out_line.getvalue().encode('utf-8'))
			out_line.close()

	def get_conv_mapping(self, to_big5 = True):
		if (to_big5 == True):
			if (len(self.gb2big5_mapping) > 0):
				return self.gb2big5_mapping

			gb2big5_table.update_gb2big5_mapping(self.gb2big5_mapping)
			gb2big5_table_1.update_gb2big5_mapping(self.gb2big5_mapping)
			gb2big5_table_2.update_gb2big5_mapping(self.gb2big5_mapping)
			
			return self.gb2big5_mapping
		else:
			if (len(self.big52gb_mapping) > 0):
				return self.big52gb_mapping

			gb2big5_table.update_big52gb_mapping(self.big52gb_mapping)
			gb2big5_table_1.update_big52gb_mapping(self.big52gb_mapping)
			gb2big5_table_2.update_big52gb_mapping(self.big52gb_mapping)
			
			return self.big52gb_mapping

if __name__ == '__main__':
	a = GB2Big5()
	f = open("1.html","r")
	f1 = open("2.html","w")
	
	a.convert(f, f1, False)
