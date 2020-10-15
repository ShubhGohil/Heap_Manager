from socket import *
import sys
import threading
import os
import time
from collections import deque

month = { 'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12 }

file_extension = {'.html':'text/html', '.txt':'text/plain', '.png':'image/png', '.gif': 'image/gif', '.jpg':'image/jpg', '.ico': 'image/x-icon', '.php':'application/x-www-form-urlencoded', '': 'text/plain', '.jpeg':'image/webp', '.pdf': 'application/pdf', '.js': 'application/javascript', '.css': 'text/css', '.mp3' : 'audio/mpeg'}


serverport = 1234 #server port number
socket = socket(AF_INET, SOCK_STREAM) #create a socket
socket.bind(("", serverport)) #bind the server with ip and port
socket.listen(50) #No. of connectinos allowed to queue

'''def content_type(path):
	check=path.split('/')[-1]'''
	

def error_message(code):
	query = status_code(code)

	response=""
	response+="<html>\n"
	response+="<head><title>"+query[13:]+"</title></head>\n"
	response+="<body>\n"
	response+="<h1>"+query[9:]+"</h1>\n"
	
	if code==304:
		response+="<p>The entity was not modified on the server.</p>\n"
	elif code==400:
		response+="<p>The server was unable to understand your request.</p>\n"
	elif code==405:
		response+="<p>The server was unable to solve your query due to unfamilier method.</p>\n"
	elif code==500:
		response+="<p>Some internal server error occured.</p>\n"
	elif code==415:
		response+="<p>The entity had Unsupported Media Type not available on server.</p>\n"
		
	response+="</body>\n"
	response+="</html>"
	
	return response

#returns the proper status code
def status_code(code):
	if code==200:
		return "HTTP/1.1 200 OK\n"
	if code==201:
		return "HTTP/1.1 201 Created\n"
	if code==202:
		return "HTTP/1.1 202 Accepted\n"
	if code==204:
		return "HTTP/1.1 204 No Content\n"	
	if code==304:
		return "HTTP/1.1 304 Not Modified\n"
	if code==400:
		return "HTTP/1.1 400 Bad Request\n"
	if code==405:	
		return "HTTP/1.1 405 Method Not Allowed\n"
	if code==404:
		return "HTTP/1.1 404 Not Found\n"
	if code==403:
		return "HTTP/1.1 403 Forbidden\n"
	if code==415:
		return "HTTP/1.1 415 Unsupported Media Type\n"
	if code==505:
		return "HTTP/1.1 505 HTTP Version Not Supported\n" 
	else:
		return "HTTP/1.1 500 Internal Server Error\n"


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
	internet_std_time+="GMT\n"

	return internet_std_time #Date header


#conditional_get check for if_modified_since	
def compare_time_if_modified(path, given_time):

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


#GET
def get_method(clientsocket, method, path, header_list):
	response_headlist=deque() #stores response headers
	response_message=''  #stores the message to be sent from server
	header_dict={} #stores the request headers with its content
	display_headers='' #stores the complete response to be sent
	statuscode=200 #stores the status code (let default be 200)
	isdirectory = 0
	isfile = 0
	conditional_get = 0
	
	for header in header_list: #extracts each headers and its value
		temp=header.split(':')
		header_dict[temp[0]] = temp[1]

	abs_path = os.getcwd()+path #stores the complete path of requested file or directory

#creates message to be sent
	if os.path.exists(abs_path): #check if path is valid
		if os.path.isfile(abs_path): #checks if file or not
			if os.access(abs_path, os.R_OK) and os.access(abs_path, os.W_OK): #check for read write permission of a file or dir
				#filename = abs_path.split('/')[-1]
				try:
					fd = open(abs_path, 'r')
					file_content = fd.read() #read contents of file
					fd.close()
					file_length = sys.getsizeof(response_message) #get the size of response (need to modify should contain length of headers+message)
					isfile = 1
				except:
					statuscode = status_code(500)
					#pass #500 Internal Server ERROR
				
			else: 
				statuscode=status_code(403)
				
		elif os.path.isdir(abs_path):
		
			dir_list=os.listdir(abs_path)
			isdirectory = 1

		else: 
			statuscode=status_code(415)
	else:
		statuscode=status_code(404)

#create response headers
	for header in header_dict:
		if header=="Host":
			response_headlist.append("Date: " + getdatetime())

		#'''elif header=="Accept": 
		#if does not satisfy this condition 406 Not Acceptable should be sent in response
		#	accept_type = header_dict[header].split(",")
						
		#	response_headers.append("Content-Type: ")
		#	pass'''
		elif header=='User-Agent':
			response_headlist.append("Server: Exite/0.1 Ubuntu\n")
			
		elif header=='Accept-Language':
			response_headlist.append("Content-Language: en\n")
						
		elif header=='Accept-Encoding':
			response_headlist.append("Content-Encoding: "+ header_dict["Accept-Encoding"] +"\n")
			
		elif header=='Cookie':
			pass
		elif header=='Accept-Charset':
			pass
		elif header=='Authorization':
			pass
		elif header=="Content-MD5":
			pass
		elif header=='If-Modified-Since': 
		#if the file is modified after the given date then only send the response message 
		#with 200 response else 304
			if statuscode==200:
				conditional_get = compare_time_if_modified(abs_path, header_dict['If-Modified-Since'])
				if conditional_get:
					response_headlist.append("Last-Modified: " + getdatetime(abs_path))
				else:
					statuscode = 304
				
		elif header=='If-Range':
			pass
		#elif header=='If-Unmodified-Since':
		#	if statuscode==200:
		#		unconditional_get = compare_time_if_modified(abs_path, header_dict['If-UnModified-Since'])
		#		if not unconditional_get:
		else:
			continue
		
	response_headlist.appendleft(status_code(statuscode))

	if statuscode==200:
		Content-Type: text/html; charset=UTF-8
		if isfile:
			message="<html>\n"
			message+="<head><title>Successfull Response</title></head>\n"
			message+="<body>\n"
			message+="<p>"+filecontent+"</p>\n"
			message+="</body>\n"
			message+="</html>"
		elif isdirectory:
			pass
		
	else:
		entity_body = error_response(statuscode)

	entity_headers=''
	for r in response_headlist:
		entity_headers+=r+"\n"
	entity_headers+="\n"
				
	response = entity_headers + entity_body
	#print(response)
	clientsocket.send(response.encode())
	clientsocket.close()


#first function called to accept the headers from client and checks the method requested
def client_request(clientsocket, address):

	statuscode=200
	message = clientsocket.recv(4096) #accept the headers
	message = message.decode('utf-8') #decode the input 
		
	requests = message.split('\r\n\r\n') #get the message string
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
		date=getdatetime()
		message="<html>\n"
		message+="<head><title>Error</title></head>\n"
		message+="<body>\n"
		message+="<h1>"+status_code(500)[9:]+"</h1>"
		message+="<p>The http version is not supported by the server.</p>\n"
		message+="</body>\n"
		message+="</html>"
		content_length = sys.getsizeof(message)
		
		headers=status_code(500)
		headers+="Server: My Server\n"
		headers+=date
		headers+="Content-Length: "+str(content_length)+"\n"
		headeres+="Content-Type: text/html; charset=iso-8859-1\n"
		response=headers+message
		clientsocket.send(response.encode())
		clientsocket.close()
		
while True:

	connectionsocket, addr = socket.accept()
	t1 = threading.Thread(target=client_request, args=(connectionsocket, addr))
	t1.start()


"""
create some html trail files
create a server log

os.path.split
os.path.textsplit


Request headers:
Host, User-Agent, Accept, Accept-Language, Accept-Encoding, Referer, Connection, Cookie, 

Respose Header:
Date, Server, X-Powered-By, Transfer_Encoding, Content_Type, Link, Content-Type, Content-Encoding, Set-Cookie


Response
HTTP/1.1 statuscode OK
Date
Content-Type
Content-Length

Accept - Content-Type
User_Agent - Server
Accept-Language - Content-Language
Connection - Connection
Server
Status


file_type = {'text/html': '.html','text/plain': '.txt', 'image/png': '.png', 'image/gif': '.gif', 'image/jpg': '.jpg','image/x-icon':'.ico', 'image/webp': '.jpeg', 'application/x-www-form-urlencoded':'.php', 'image/jpeg': '.jpeg', 'application/pdf': '.pdf', 'audio/mpeg': '.mp3', 'video/mp4': '.mp4'}


#https://github.com/roopi7760/WebServer/blob/master/Server.py
#https://github.com/sm8799/HTTP-Web-Server/blob/master/webserver.py\ """
