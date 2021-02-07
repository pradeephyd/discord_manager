import time


class CONNECTION:
	def __init__(self, client, server):
		self.conn = client[0]
		self.host = client[1][0]
		self.port = client[1][1]

		self.times = [client[2], time.time()]

		self.discord = self.server.discord

		self.data = self.server.data

		self.discord_data = discord.data

	def login_discord(self):
		self.discord.login()
