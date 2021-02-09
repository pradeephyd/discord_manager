class BOT:
	def __init__(self, data, pr=print, inp=input, save=False):
		self.data = data
		self.pr = pr
		self.inp = inp
		self.save = save
		self.last_said = ""
		self.last_reply = ""

	def get_reply(self, message):
		for c in self.data:
			if message == c[0]:
				return c[1]
		return False

	def save_data(self):
		if self.save:
			self.save(self.data)

	def get_new_reply(self, message):
		reply = self.inp("Desconozco ({}). Como deberia responder?".format(message))
		self.data.append([message, reply])
		self.save_data()

	def auto(self):
		while True:
			message = self.inp()
			if not message == self.last_said and not message == self.last_reply:
				self.reply(message)

	def reply(self, message):
		reply = self.get_reply(message)

		if not reply:
			self.get_new_reply(message)
		else:
			self.pr(reply)

