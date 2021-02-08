from code.send_recv import * 
host = "192.168.1.92"
port = 5656

m = SEND_RECV(host=host, port=port)

while True:
	m.react()