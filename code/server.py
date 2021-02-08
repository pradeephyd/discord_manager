from code.connection import *
from threading import Thread as th
import time
import socket
from pickle import dumps

class SERVER:
	def __init__(self, host, port, DISCORD, DATA):
		self.host = host
		self.port = port

		#OBJECT TO CONTROLL DISCORD
		self.discord = DISCORD

		#OBJECT TO LOAD AND SAVE DATA
		self.data = DATA()

		self.data.load()

		#SERVER SOCKET
		self.socket = False

		#THREADS USED BY CLIENTS
		self.threads = []

		#QUEUE
		self.waiting = []
		self.new_waiting = True

	def get_cookies(self):
		return self.data.cookies


	def save_cookies(self, cookies):
		self.data.cookies = cookies
		self.data.save()

	def yn(self, message, pr=print, inp=input):
		if "y" in inp("{}? Y/n".format(message)).lower():
			return True
		else:
			return False

	def get_log_info(self, pr=print, inp=input):
		username = inp("Console username: ")
		password = inp("Console password: ")

		discord_email = inp("Discord email: ")
		discord_password = inp("Discord password: ")

		return {"discord":{"email":discord_email, "password":discord_password, "logged":False}, "username":username, "password":password}

	def create_new_account(self, pr=print, inp=input):
		account_info = self.get_log_info(pr=pr, inp=inp)

		self.save_new_account(account_info)

		return account_info

	def save_account(self, account_info, cookies):
		self.save_cookies(cookies)
		for a in self.data.profiles:
			if a["username"] == account_info["username"]:
				self.data.profiles[self.data.profiles.index(a)] = account_info

		self.data.save_profiles()

	def save_new_account(self, account_info):
		self.data.profiles.append(account_info)

		self.data.save_profiles()

	def get_account_info(self, username, password, pr=print, inp=input):
		for a in self.data.profiles:
			if a["username"] == username:
				for i in range(5):
					if a["password"] == password:
						return a, self.get_cookies()
					else:
						pr("Incorrect password")
						password = inp("Retry({}): ".format(i))
				pr("Max tries try again later")
				return False, False

		pr("Account doesnt exist")
		if self.yn("Create account", pr=pr, inp=inp):
			return self.create_new_account(pr=pr, inp=inp), dumps([])
		else:
			return False, False

	def start_server(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((self.host, self.port))
		self.start_listening()


	def start_listening(self):
		self.socket.listen()
		self.listen_new_connections()


	def listen_new_connections(self):
		while True:
			conn, addr = self.socket.accept()
			client = [conn, addr, time.time()]
			waiting_thread = th(target=self.wait, args=(client,))
			waiting_thread.start()
			self.threads.append(waiting_thread)


	def wait(self, client):
		self.waiting.append(client[2])
		while not self.waiting[0] == client[2] and not self.new_waiting:
			time.sleep(0.01)
		self.new_waiting = False
		del self.waiting[0]
		self.establish_connection(client)


	def establish_connection(self, client):
		connection = CONNECTION(client, self)
		connection.start()