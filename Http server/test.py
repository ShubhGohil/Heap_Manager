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
	response_headers=[] #stores response headers
	response=''  #stores the message to be sent from server
	header_dict={} #stores the request headers with its content
	display_headers='' #stores the complete response to be sent
	statuscode=0 #stores the status code
	for header in header_list: #extracts each headers and its value
		temp=header.split(':')
		header_dict[temp[0]] = temp[1]
	abs_path = os.getcwd()+path #stores the complete path of requested file or directory
	if os.path.exists(abs_path): #check if path is valid
		if os.path.isfile(abs_path): #checks if file or not
			if os.access(abs_path, os.R_OK) and os.access(abs_path, os.W_OK): #check for read write permission of a file or dir
				#filename = abs_path.split('/')[-1]
				try:
					fd = open(abs_path, 'r') 
					file_content = fd.read() #read contents of file
					file_length = os.path.getsize(abs_path) #get the size of file
					response+="<html>"
					response+="<head><link rel=\"stylesheet\" href=\"resource://content-accessible/plaintext.css\"></head>"
					response+="<body>"+file_content+"</body>"
					response+='</html>'
				except:
					pass #500 Internal Server ERROR
				
				for header in header_dict:
					if header=="Host":
						pass
					'''elif header=="Accept": #if does not satisfy this condition 406 Not Acceptable should be sent in response
						accept_type = header_dict[header].split(",")
						
						response_headers.append("Content-Type: ")
						pass'''
					elif header=='User-Agent':
						response_headers.append("Server: ABcd/0.1 Ubuntu")
						pass
					elif header=='Accept-Language':
						response_headers.append("Content-Language: en-US")
						pass
					elif header=='Accept-Encoding':
						pass
					elif header=='Referer':
						pass
					elif header=='Connection':
						pass
					elif header=='Cookie':
						pass
					elif header=='Accept-Charset':
						pass
					elif header=='Authorization':
						pass
					elif header=='From': #for email
						pass
					elif header=='If-Match':
						pass
					elif header=='If-Modified-Since': #if the file is modified after the given date then only send the response message with 200 response else 304
						pass
					elif header=='If-None-Match':
						pass
					elif header=='If-Range':
						pass
					elif header=='If-Unmodified-Since':
						pass


			#else: 403 Forbidden
		#elif os.path.isdir(abs_path):
		
		#else: 415 Unsupported Media Type
	else:
		# 404 Not Found
			

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


