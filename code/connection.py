import time
from code.send_recv import *

class CONNECTION:
	def get_account_info(self):
		return self.server.get_account_info(self.username, self.password, pr=self.pr, inp=self.inp)

	def start(self):
		self.login()

		account_info, cookies = self.get_account_info()

		if account_info:

			self.discord = self.server.discord(account_info, cookies)

			self.discord.open_web()

			account_info, cookies = self.discord.load_account()

			self.server.save_account(account_info, cookies)

			while True:
				command = self.inp("Command: ").lower()

				if command == "chats":
					self.pr(self.discord.get_chat_names())
				else:
					if command == "go_to_chat":
						self.discord.go_to_chat(self.inp("Chat: "))
					else:
						if command == "send":
							self.discord.send_message(self.inp("Message: "))
						else:
							if command == "pesado":
								self.discord.go_to_chat("JNL500X")
								while True:
									self.discord.send_message(str(time.time()))
									time.sleep(1)
							else:
								if command == "i":
									self.discord.bot_answer_chat()
								else:
									if command == "messages":
										question, answer = self.discord.get_messages()
										self.pr("Question: {} \nAnswer: {}".format(question, answer))
									else:
										if command == "last_message":
											self.pr(self.discord.get_newest_message())

	def login(self):
		self.username = self.inp("Username: ")
		self.password = self.inp("Password: ")

	def __init__(self, client, server):
		self.conn = client[0]
		self.host = client[1][0]
		self.port = client[1][1]

		self.username = False
		self.password = False

		self.times = [client[2], time.time()]

		self.server = server

		self.send_recv = SEND_RECV(self.conn)

		self.pr = self.send_recv.pr
		self.inp = self.send_recv.inp