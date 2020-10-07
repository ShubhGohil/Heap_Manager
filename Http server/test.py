from socket import *
import sys
import threading

serverport = 1234

socket = socket(AF_INET, SOCK_STREAM)
socket.bind(("", serverport))
socket.listen(50)


def client_request(clientsocket, address):
	#while True:
	message = connectionsocket.recv(4096)
	try:
		message = message.decode('utf-8')
		requests = message.split('\n')
	except UnicodeDecodeError:
		requests = message.split('\n')
		requests = requests[0].decode(errors = 'ignore')
	first_line = requests[0].split(' ')
	method = first_line[0]
	path = first_line[1]
	version = first_line[2]
	print(method, path, version)
	if method == 'GET':
		pass


while True:

	connectionsocket, addr = socket.accept()
	t1 = threading.Thread(target=client_request, args=(connectionsocket, addr))
	t1.start()


"""
create a socket
do multithreading 
create some html trail files
create a server log"""

