from socket import *
import sys
import threading
import os

serverport = 1234
socket = socket(AF_INET, SOCK_STREAM) #create a socket
socket.bind(("", serverport)) #bind the server with ip and port
socket.listen(50) #No. of connectinos allowed to queue

#GET
def get_method(clientsocket, method, path, header_list):
	response
	abs_path = os.getcwd()+path
	if os.path.exists(abs_path):
		if os.path.isfile(abs_path): #check for read write permission of a file or dir
			
		#elif os.path.isdir(abs_path):
		
		#else:
	else:
		# 400 Bad request
			

#first function called to accept the headers from client and checks the method requested
def client_request(clientsocket, address):
	complete_message=''
	while True:
		try:
			message = clientsocket.recv(4096) #accept the headers
			message = message.decode('utf-8') #decode the input 
			
			complete_message+=message #append the new header to create the complete the message
			if message=='\r\n': #an empty line denotes end of message from client
				break
		except UnicodeDecodeError:
			message = message.decode(errors = 'ignore')
			complete_message+=message
			if message=='\r\n':
				break

	requests = complete_message.split('\r\n\r\n') #get the message string
	header_list = requests[0].split('\r\n') #split each header
	first_line = header_list[0].split() #gets the first line of message
	method = first_line[0] #get the method requested
	path = first_line[1] #get the path requested
	version = first_line[2] #get the version requested

	if version=='HTTP/1.1':
		header_list.pop(0) #remove the first line since the elements were analysed
		if method == 'GET':
			get_method(clientsocket, method, path, header_list) #call get method
		#elif something:
		else:
			#raise 400 Bad Request
	else:
		#raise 505 HTTP Version Not Supported
		
		
while True:

	connectionsocket, addr = socket.accept()
	t1 = threading.Thread(target=client_request, args=(connectionsocket, addr))
	t1.start()


