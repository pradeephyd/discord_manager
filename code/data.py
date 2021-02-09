import json
from pickle import dumps, loads

class DATA:
	def __init__(self):
		self.folder = "data/"
		self.file_server = "data.json"
		self.file_server = "bot.json"
		self.file_profiles = "profiles.json"
		self.file_conf = "config.json"
		self.file_cookies = "cookies"

		self.server = {}
		self.profiles = []
		self.conf = {}
		self.cookies = dumps([])
		self.bot = []

	def l(self, file_name, default, save, type="r", load_json=True):
		try:
			content = open(self.folder + file_name, type).read()
		except:
			save()
			return default
		else:
			if load_json:
				try:
					data = json.loads(content)
				except:
					print("Error loading json data")
				else:
					return data
			else:
				return content

	def load_cookies(self):
		self.cookies = loads(self.l(self.file_cookies, self.cookies, self.save_cookies, type="rb", load_json=False))

	def load_server(self):
		self.server = self.l(self.file_server, self.server, self.save_server)

	def load_bot(self):
		self.bot = self.l(self.file_bot, self.bot, self.save_bot)

	def load_profiles(self):
		self.profiles = self.l(self.file_profiles, self.profiles, self.save_profiles)

	def load_conf(self):
		self.conf = self.l(self.file_conf, self.conf, self.save_conf)

	def load(self):
		self.load_conf()
		self.load_profiles()
		self.load_bot()
		self.load_server()
		self.load_cookies()

	def s(self, file_name, data, type="w", code_json=True):
		if code_json:
			data = json.dumps(data)

		print(self.folder, file_name, type, data)

		open(self.folder + file_name, type).write(data)

	def save_cookies(self):
		self.s(self.file_cookies, dumps(self.cookies), type="wb", code_json=False)

	def save_server(self):
		self.s(self.file_server, self.server)

	def save_bot(self):
		self.s(self.file_bot, self.bot)

	def save_profiles(self):
		self.s(self.file_profiles, self.profiles)

	def save_conf(self):
		self.s(self.file_conf, self.conf)

	def save(self):
		self.save_conf()
		self.save_profiles()
		self.save_bot()
		self.save_server()
		self.save_cookies()