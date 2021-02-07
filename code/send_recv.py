from time import sleep
import json
from threading import Thread as th

class SEND_RECV:
	def stop(self):
		self.recv_messages = False

	def send_command(self, command, message=False, message1=False, message2=False, message3=False, message4=False, message5=False):
		if not message:
			message = ""

		message = self.command_decor + command + message

		if message1:
			message += message1

		if message2:
			message += message2

		if message3:
			message += message3

		if message4:
			message += message4

		if message5:
			message += message5

		self.send(message)

	def inp(self, message=False, message1=False, message2=False, message3=False, message4=False, message5=False):
		self.send_command("INPUT", message, message1, message2, message3, message4, message5)

		return self.recv()

	def pr(self, message=False, message1=False, message2=False, message3=False, message4=False, message5=False):
		self.send_command("PRINT", message)

	def send(self, message):
		d = str(message).encode("utf-8")
		self.conn.sendall(self.send_data_slip_decor_byte + d + self.send_data_slip_decor_byte)

	def listen(self):
		while self.recv_messages:
			message = self.conn.recv(self.buffer)
			while len(message.split(self.send_data_slip_decor_byte)) < 3:
				message += self.conn.recv(self.buffer)
			self.messages.append(message)

	def recv(self):
		while self.recv_messages:
			for m in self.messages:
				d = m.decode("utf-8").replace(self.send_data_slip_decor, "")
				del self.messages[self.messages.index(m)]
				return d
			sleep(self.delay)			

	def command_to_action(self, message):
		for c in self.react_commands:
			full = self.command_decor+c[0]
			if full in message:
				return c[1](message.replace(full, ""))

	def react(self):
		message = self.recv()
		ret = self.command_to_action(message)
		if not ret == None:
			self.send(ret)

	def __init__(self, conn, buffer=2048, pr=print, inp=input):
		self.conn = conn
		self.messages = []
		self.delay = 0.01
		self.recv_messages = True
		self.buffer = buffer

		self.command_decor = "$$$$$$$$$$$$$"

		self.send_data_slip_decor = "%%%%%%%%%%%"
		self.send_data_slip_decor_byte = self.send_data_slip_decor.encode("utf-8")
		self.user_print = pr
		self.user_input = inp

		self.react_commands = [
		["INPUT", self.user_input],
		["PRINT", self.user_print]
		]

		self.listen_thread = th(target=self.listen)

		self.listen_thread.start()


