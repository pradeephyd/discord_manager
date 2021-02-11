import threading
import socket
import pickle
import cv2
import time

class SERVER:
	def setup(self):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.bind((self.host, self.port))
		self.hear()

	def hear(self):
		self.server.listen()
		while True:
			conn, addr = self.server.accept()
			print(addr, conn)
			t = threading.Thread(target=self.stream, args=(conn,))
			t.start()
			self.threads.append(t)

	def stream(self, conn):
		cap = cv2.VideoCapture("2020-12-29 22-00-16.mkv")
		ret, frame = cap.read()
		conn.send(str(len(pickle.dumps(frame))).encode("utf-8"))
		while True:
			if ret:
				self.send(frame, conn)
			ret, frame = cap.read()

	def send(self, frame, conn):
		try:
			data = pickle.dumps(frame)
		except:
			pass
		else:
			conn.send(data)

	def __init__(self, host="localhost", port=4747, buffer=1024):
		self.host = host
		self.port = port
		self.buffer = buffer
		self.threads = []

class CLIENT:
	def __init__(self, host="localhost", port=4747, buffer=1024):
		self.host = host
		self.port = port
		self.buffer = buffer
		self.video_buffer = False
		self.frames = []

	def connect(self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client.connect((self.host, self.port))
		self.video_buffer = int(self.client.recv(1024))

	def get_frame(self):
		for i in range(100000):
			for e in self.frames:
				del self.frames[0]
				return True, e
			time.sleep(0.001)
		return False, False

	def streaming(self):
		self.connect()
		t = threading.Thread(target=self.get_frames)
		t.start()
		self.show_frames()


	def show_frames(self):
		ret, frame = self.get_frame()
		while ret:
			try:
				cv2.imshow("streaming", frame)
				cv2.waitKey(1)
			except:
				pass
			else:
				print(len(self.frames))
			ret, frame = self.get_frame()
		print("Finished")

	def get_frames(self):
		data = b""
		while True:
			data += self.client.recv(self.buffer)
			l = len(data)
			if l >= self.video_buffer:
				try:
					d = data[:self.video_buffer]
					d = pickle.loads(d)
				except:
					pass
				else:
					self.frames.append(d)
					data = data[self.video_buffer:l]

