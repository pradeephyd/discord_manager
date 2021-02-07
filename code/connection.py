import time
from code.send_recv import *

class CONNECTION:

	def __init__(self, client, server):
		self.conn = client[0]
		self.host = client[1][0]
		self.port = client[1][1]

		self.times = [client[2], time.time()]

		self.discord = server.discord

		self.server = server

		#self.data = self.server.data

		#self.discord_data = discord.data

		self.send_recv = SEND_RECV(self.conn)

		self.pr = self.send_recv.pr
		self.inp = self.send_recv.inp

	def get_log_info(self):
		self.username = self.inp("Username: ")
		self.password = self.inp("Password: ")

	def start(self):
		self.get_log_info()