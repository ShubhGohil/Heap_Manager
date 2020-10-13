from socket import *
import sys
import threading
import os
import time
from collections import deque

month = { 'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12 }

serverport = 1234 #server port number
socket = socket(AF_INET, SOCK_STREAM) #create a socket
socket.bind(("", serverport)) #bind the server with ip and port
socket.listen(50) #No. of connectinos allowed to queue

#returns the proper status code
def status_code(code):
	if code==200:
		return "HTTP/1.1 200 OK"
	if code==201:
		return "HTTP/1.1 201 Created"
	if code==202:
		return "HTTP/1.1 202 Accepted"
	if code==204:
		return "HTTP/1.1 204 No Content"	
	if code==304:
		return "HTTP/1.1 304 Not Modified"
	if code==400:
		return "HTTP/1.1 400 Bad Request"
	if code==405:	
		return "HTTP/1.1 405 Method Not Allowed"
	if code==404:
		return "HTTP/1.1 404 Not Found"
	if code==403:
		return "HTTP/1.1 403 Forbidden"
	if code==415:
		return "HTTP/1.1 415 Unsupported Media Type"
	if code==505:
		return "HTTP/1.1 505 HTTP Version Not Supported" 
	else:
		return "HTTP/1.1 500 Internal Server Error"


#get the last modified time of the file given, else return current time 
def getdatetime(path=None):
	if path:
		file_modification_time=os.path.getmtime(path) #provides last modification time from epoch in sec 
		readable_time = time.ctime(file_modification_time) #displays current date and time
	else:
		readable_time = time.ctime()
	separate = readable_time.split()
	separate[0]+=","
	
	order="02143" #order in which the readable format has to be arranged to get standard internet format
	internet_std_time=''
	
	for i in order:
		internet_std_time = internet_std_time + separate[int(i)] + " "
	internet_std_time+="GMT"

	return "Date: " + internet_std_time #Date header


#conditional_get check for if_modified_since	
def compare_time_if_modified(path, given_time):
	try:
		file_modification_time=os.path.getmtime(path)
		readable_time = time.ctime(file_modification_time)
		separate = readable_time.split()
		
		#print("Readable time", readable_time)
		
		hour=separate[3].split(":")[0]
		minute=separate[3].split(":")[1]
		second=separate[3].split(":")[2]
	
		mod_time = datetime.datetime(int(separate[4]), month[separate[1]], int(separate[2]), int(hour), int(minute), int(second))
	
		separate = given_time.split()
	
		#print("Check_time",check_time)	
		
		hour=separate[4].split(":")[0]
		minute=separate[4].split(":")[1]
		second=separate[4].split(":")[2]
		
		giv_time = datetime.datetime(int(separate[3]), month[separate[2]], int(separate[1]), int(hour), int(minute), int(second))
		
		if mod_time >= giv_time: #if the modified file time is ahead than time given than return True
			return True
		else:
			return False
	except:
		return "error"


#GET
def get_method(clientsocket, method, path, header_list):
	response_headlist=deque() #stores response headers
	response_message=''  #stores the message to be sent from server
	header_dict={} #stores the request headers with its content
	display_headers='' #stores the complete response to be sent
	statuscode=200 #stores the status code (let default be 200)
	
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
					fd.close()
					response_message+="<html>\n"
					response_message+="<head><link rel=\"stylesheet\" href=\"resource://content-accessible/plaintext.css\"></head>\n"
					response_message+="<body>"+file_content+"</body>\n"
					response_message+='</html>\n\n'
					file_length = sys.getsizeof(response_message) #get the size of response (need to modify should contain length of headers+message)

				except:
					statuscode = status_code(500)
					#pass #500 Internal Server ERROR
				
				for header in header_dict:
					if header=="Host":
						response_headlist.append(getdatetime(abs_path))
						response_headlist.append("Server: ABcd/0.1 Ubuntu")
						response_headlist.append("Content-Length: " + str(file_length))
					#'''elif header=="Accept": 
					#if does not satisfy this condition 406 Not Acceptable should be sent in response
					#	accept_type = header_dict[header].split(",")
						
					#	response_headers.append("Content-Type: ")
					#	pass'''
					elif header=='User-Agent':
						pass
						
					elif header=='Accept-Language':
						response_headlist.append("Content-Language: en-US")
						
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
					elif header=='If-Modified-Since': 
					#if the file is modified after the given date then only send the response message 
					#with 200 response else 304
						pass
					elif header=='If-None-Match':
						pass
					elif header=='If-Range':
						pass
					elif header=='If-Unmodified-Since':
						pass
					else:
						continue
				
				response_headlist.appendleft(status_code(statuscode))
					
				response_headers=''
				for r in response_headlist:
					response_headers+=r+"\n"
				response_headers+="\n"
				
				response = response_headers + response_message
				#print(response)
				clientsocket.send(response.encode())
				clientsocket.close()
			else: 
				statuscode=status_code(403)
				
		elif os.path.isdir(abs_path):
			dir_list=os.listdir(abs_path)
			
			response_message+="<html>\n"
			response_message+="<head><link rel=\"stylesheet\" href=\"resource://content-accessible/plaintext.css\"></head>\n"
			response_message+="<body><h1>Directory Listing</h1><ul>\n"
			for element in dir_list:
				response_messasge+="<li>"+element+"</li>\n"
			response_message+="</ul></body>\n"
			response_message+='</html>\n\n'
		
		else: 
			statuscode=status_code(415)
	else:
		statuscode=status_code(404)
		

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
			pass
	else:
		#raise 505 HTTP Version Not Supported
		pass
		
while True:

	connectionsocket, addr = socket.accept()
	t1 = threading.Thread(target=client_request, args=(connectionsocket, addr))
	t1.start()


