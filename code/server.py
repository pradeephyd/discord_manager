from code.connection import *
from threading import Thread as th
import time
import socket

class SERVER:
	def __init__(self, host, port, DISCORD, DATA):
		self.host = host
		self.port = port

		#OBJECT TO CONTROLL DISCORD
		self.discord = DISCORD

		#OBJECT TO LOAD AND SAVE DATA
		self.data = DATA()

		#SERVER SOCKET
		self.socket = False

		#THREADS USED BY CLIENTS
		self.threads = []

		#QUEUE
		self.waiting = []
		self.new_waiting = True


	def yn(self, message, pr=print, inp=input):
		if "y" in inp("{}? Y/n".format(message)).lower():
			return True
		else:
			return False

	def get_log_info(self, pr=print, inp=input):
		email = inp("Discord email: ")
		password = inp("Discord password: ")
		return {"email":email, "password":password, "cookies":dumps([])}

	def create_new_account(self, pr=print, inp=input):
		account_info = self.get_log_info(pr=pr, inp=inp)

		self.save_new_account(account_info)

		return account_info

	def save_new_account(self, account_info):

		self.data.profiles.append(account_info)

	def get_account_info(self, username, password, pr=print, inp=input):
		for a in self.data.profiles:
			if a["username"] == username:
				for i in range(5):
					if a["password"] == password:
						return a
					else:
						pr("Incorrect password")
						password = input("Retry({}): ".format(i))
				pr("Max tries try again later")

		pr("Account doesnt exist")
		if self.yn("Create account", pr=pr, inp=inp):
			return self.create_new_account(pr=pr, inp=inp)
		else:
			return False

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