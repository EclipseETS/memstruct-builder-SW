class message:

	def __init__(self):
		self.name = ""
		self.id = 0
		self.signal = []
		self.signal_cnt = 0

	def set_params(self, message_name, message_id):
		self.name = message_name
		self.id = message_id

	def add_signal(self, signal):
		self.signal.append(signal)
		self.signal_cnt += 1

	def print_callback(self, fo):
		for sig in self.signal:
			sig.print_callback(fo)

	def print_signal_enum(self, fo):
		for sig in self.signal:
			sig.print_enum(fo)

	def print_enum(self, fo, last_id):
		if (last_id + 1 == self.id):
			fo.write("\t{},\n".format(self.name))
		else:
			fo.write("\t{} = {},\n".format(self.name, self.id))
		last_id = self.id

	def print_para_macro(self, fo, last):
		cnt = len(self.signal)
		for index, sig in enumerate(self.signal, start = 1):
			if(last and cnt == index):
				sig.print_para_macro(fo, 1)
			else:
				sig.print_para_macro(fo, 0)

	def print_message_def(self, fo, board_name, little_endian):
		fo.write("\t{\n")
		fo.write("\t\tID_OFFSET_{} + {}, /* CAN-Identifier */\n".format(board_name, self.name))
		fo.write("\t\tM_{}_TXRX, /* Message Type */\n".format(board_name))

		fo.write("\t\t")
		for index, sig in enumerate(self.signal, start = 1):
			if(index == self.signal_cnt):
				fo.write("sizeof({}),".format(sig.type))
			else:
				fo.write("sizeof({}) + ".format(sig.type))
		fo.write(" /* DLC of Message */\n")

		fo.write("\t\t{}, /* No. of Links */\n".format(self.signal_cnt))
		fo.write("\t\t{\n")

		byte_pos = "0"

		for index, sig in enumerate(self.signal, start = 1):
			if(index == self.signal_cnt):
				sig.print_definition(fo, byte_pos, 1, little_endian)
			else:
				sig.print_definition(fo, byte_pos, 0, little_endian)
			byte_pos = byte_pos + " + sizeof({})".format(sig.type)

		fo.write("\t\t}\n")
		fo.write("\t},\n")

	def print_debug(self):
		print self.name
		print self.id
		print self.signal_cnt

		for sig in self.signal:
			sig.print_debug()