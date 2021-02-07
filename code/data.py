import json
class DATA:
	def __init__(self):
		self.folder = "data/"
		self.file_server = "data.json"
		self.file_profile = "profile.json"
		self.file_conf = "config.json"

		self.server = {}
		self.profile = {}
		self.conf = {}

	def l(self, file_name, default, save):
		try:
			content = open(self.folder + file_name, "r").read()
		except:
			save()
			return default
		else:
			try:
				data = json.loads(content)
			except:
				print("Error loading json data")
			else:
				return data

	def load_server(self):
		self.server = self.l(self.file_server, self.server, self.save_server)

	def load_profile(self):
		self.profile = self.l(self.file_profile, self.profile, self.save_profile)

	def load_conf(self):
		self.conf = self.l(self.file_conf, self.conf, self.save_conf)

	def load(self):
		self.load_conf()
		self.load_profile()
		self.load_server()

	def s(self, file_name, data):
		data = json.dumps(data)

		open(self.folder + file_name, "w").write(data)

	def save_server(self):
		self.s(self.file_server, self.server)

	def save_profile(self):
		self.s(self.file_profile, self.profile)

	def save_conf(self):
		self.s(self.file_conf, self.conf)

	def save(self):
		self.save_conf()
		self.save_profile()
		self.save_server()