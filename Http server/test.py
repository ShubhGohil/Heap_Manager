from socket import *
import sys
import threading

serverport = 1234

socket = socket(AF_INET, SOCK_STREAM)
socket.bind(("", serverport))
socket.listen(50)

h_flag=0
def client_request(clientsocket, address):
	complete_message=''
	while True:
		message = clientsocket.recv(4096)
		message = message.decode('utf-8')
		
		complete_message+=message
		if message=='\r\n':
			break
		'''except UnicodeDecodeError:
			requests = message.split('\n')
			requests = requests[0].decode(errors = 'ignore')'''
	requests = complete_message.split('\r\n\r\n')
	header_list = requests[0].split('\r\n')
	first_line = header_list[0].split()
	method = first_line[0]
	path = first_line[1]
	version = first_line[2]
	#print(method, path, version)
	if method == 'GET':
		pass
	

while True:

	connectionsocket, addr = socket.accept()
	t1 = threading.Thread(target=client_request, args=(connectionsocket, addr))
	t1.start()
'''complete_message=''	
while True:
	message = input()
	message=message.encode()
	message = message.decode('utf-8')
	print(message)
	complete_message+=message
	if message=='\n':
		break
print(complete_message)
header_list=complete_message.split('\n')
first_line = header_list[0].split()
method = first_line[0]
path = first_line[1]
version = first_line[2]
	
print(method, path, version)
'''
