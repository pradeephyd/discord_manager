from code.send_recv import * 
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("192.168.1.92", 5656))

m = SEND_RECV(s)

while True:
	m.react()