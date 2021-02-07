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