from socket import *
import sys
import threading
import os
import time
from collections import deque
import datetime


month = { 'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12 }

file_extension = {'html':'text/html', 'txt':'text/plain', 'png':'image/png', 'gif': 'image/gif', 'jpg':'image/jpg', 'ico': 'image/x-icon', 'php':'application/x-www-form-urlencoded', '': 'text/plain', 'jpeg':'image/webp', 'pdf': 'application/pdf', 'js': 'application/javascript', 'css': 'text/css', 'mp3' : 'audio/mpeg'}


serverport = 1234 #server port number
socket = socket(AF_INET, SOCK_STREAM) #create a socket
socket.bind(("", serverport)) #bind the server with ip and port
socket.listen(50) #No. of connectinos allowed to queue

#reads the file according to given condition
def readfile(abs_path, statusnumber, size=0, start=0, end=sys.maxsize):
	
	try:
		fd = open(abs_path, 'rb')
		entity_body = fd.read()
		#get the size of response
		file_length = sys.getsizeof(entity_body)
		if size != 0 and end<file_length:
			entity_body = entity_body[start:end+1] #read contents of file
			statusnumber=206
		fd.close()
	except:
		statusnumber = 500
			 
	return entity_body, file_length, statusnumber 

#gives the type of file
def content_type(path):
	try:
		check=path.split('/')[-1]
		extension=check.split('.')[-1]
		if extension in file_extension.keys():
			content_type = file_extension[extension]
			return content_type
		else:
			return None
	except:
		return None
	
#error message if an error occur
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
	elif code==404:
		response+="<p>The requested entity is not available.</p>\n"
	elif code==505:
		response+="<p>The HTTP version is not supported by the server.</p>\n"
		
	response+="</body>\n"
	response+="</html>"
	
	return response

#returns the proper status code
def status_code(code):
	if code==200:
		return "HTTP/1.1 200 OK"
	elif code==201:
		return "HTTP/1.1 201 Created"
	elif code==202:
		return "HTTP/1.1 202 Accepted"
	elif code==204:
		return "HTTP/1.1 204 No Content"
	elif code==206:
		return "HTTP/1.1 206 Partial Content"	
	elif code==304:
		return "HTTP/1.1 304 Not Modified"
	elif code==400:
		return "HTTP/1.1 400 Bad Request"
	elif code==405:	
		return "HTTP/1.1 405 Method Not Allowed"
	elif code==404:
		return "HTTP/1.1 404 Not Found"
	elif code==403:
		return "HTTP/1.1 403 Forbidden"
	elif code==415:
		return "HTTP/1.1 415 Unsupported Media Type"
	elif code==505:
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

	return internet_std_time #Date header


#conditional_get check for if_modified_since	
def compare_time_if_modified(path, given_time):

	file_modification_time=os.path.getmtime(path)
	readable_time = time.ctime(file_modification_time)
	separate = readable_time.split()
	
	#print("Readable time", readable_time)
	#print("Separate current time", separate)
	hour=separate[3].split(":")[0]
	minute=separate[3].split(":")[1]
	second=separate[3].split(":")[2]

	mod_time = datetime.datetime(int(separate[4]), month[separate[1]], int(separate[2]), int(hour), int(minute), int(second))
	
	separate = given_time.split()

	#print("Check_time",check_time)	
	#print("Separate given time", separate)
	
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
	statusnumber=200 #stores the status code (let default be 200)
	isdirectory = 0
	isfile = 0 
	conditional_get = 0 #condition for if-modified
	size = 0 #bytes of file to be read
	range_head = 0 #flag for range headers
	start, end = 0, 0 #for range headers to determine end and start bytes
	
	for header in header_list: #extracts each headers and its value
		if header[0:17].lower()=="if-modified-since":
			header_dict[header[:17].lower()] = header[18:]
		elif header[0:8].lower()=='if-range':
			header_dict[header[:8].lower()] = header[9:]
		else:
			temp=header.split(':')
			if temp[0]=="range":
				size = int(temp[1])
			header_dict[temp[0].lower()] = temp[1]
		
	abs_path = os.getcwd()+path #stores the complete path of requested file or directory

	if 'range' in header_dict.keys():
		if 'if-range' in header_dict.keys():
			if compare_time_if_modified(abs_path, header_dict['if-range']):
				start = int(header_dict['range'].split('-')[0].replace(' ',''))
				end = int(header_dict['range'].split('-')[1])
				size= end - start + 1
				range_head = 1
				'''print(start, "start")
				print(end, "end")
				print(size, "size")'''

		else:
			start = int(header_dict['range'].split('-')[0])
			end = int(header_dict['range'].split('-')[1])
			size= end - start + 1
			range_head = 1

#creates message to be sent
	if os.path.exists(abs_path): #check if path is valid
		if os.path.isfile(abs_path): #checks if file or not
		#check for read write permission of a file or dir
			if os.access(abs_path, os.R_OK) and os.access(abs_path, os.W_OK): 
			
				entity_body, file_length, statusnumber = readfile(abs_path, statusnumber, size, start, end)
				if range_head:
					response_headlist.append("Accept-Range: bytes")
					response_headlist.append("Content-Range: bytes " + header_dict['range']+'/'+str(file_length))
				
			else: 
				statusnumber=403
				
		elif os.path.isdir(abs_path):
			if os.access(abs_path, os.R_OK) and os.access(abs_path, os.W_OK):
		
				dir_list=os.listdir(abs_path)
				if "index.html" in dir_list:
					if abs_path.endswith('/'):
						if os.access(abs_path+"index.html", os.R_OK) and os.access(abs_path+"index.html", os.W_OK):
							entity_body, file_length, statusnumber = readfile(abs_path+"index.html", statusnumber, size, start, end)
							if range_head:
								response_headlist.append("Accept-Range: bytes")
								response_headlist.append("Content-Range: bytes " + header_dict['range']+'/'+str(file_length))

						else:
							isdirectory = 1
							
					else:
						if os.access(abs_path+"/index.html", os.R_OK) and os.access(abs_path+"/index.html", os.W_OK):
							entity_body, file_length, statusnumber = readfile(abs_path+"/index.html", statusnumber, size, start, end)
							if range_head:
								response_headlist.append("Accept-Range: bytes")
								response_headlist.append("Content-Range: bytes " + header_dict['range']+'/'+str(file_length))
							
							isdirectory = 1
				else:	
					isdirectory = 1
			else:
				statusnumber=403
		else: 
			statusnumber=415
	else:
		statusnumber=404
			
	
#create response headers

	for header in header_dict:
		if header.lower()=="host":
			response_headlist.append("Date: " + getdatetime())
	
			'''elif header=="Accept": 
		if does not satisfy this condition 406 Not Acceptable should be sent in response
			accept_type = header_dict[header].split(",")
						
			response_headers.append("Content-Type: ")
			pass'''
		elif header=='user-agent':
			response_headlist.append("Server: Exite/0.1 Ubuntu")
				
		elif header=='accept-language':
			if header_dict['accept-language']==' en-US' or header_dict['accept-language'].split(',')[0]==' en-US':
				response_headlist.append("Content-Language: en-US")
			
		elif header=='accept-encoding' and statusnumber==200:
			response_headlist.append("Content-Encoding: identity")
				
		elif header=='cookie':
			pass

		elif header=='authorization' and statusnumber==200:
			pass
		elif header=="content-md5" and statusnumber==200:
			pass
		elif header=='if-modified-since' and statusnumber==200:
			conditional_get = compare_time_if_modified(abs_path, header_dict[header])
			if conditional_get:
				response_headlist.append("Last-Modified: " + getdatetime(abs_path))
			else:
				statusnumber = 304
					
		#elif header=='If-Unmodified-Since':
		#	if statuscode==200:
		#		unconditional_get = compare_time_if_modified(abs_path, header_dict['If-UnModified-Since'])
		#		if not unconditional_get:
		else:
			continue
		
	response_headlist.appendleft(status_code(statusnumber))
	
	if statusnumber==200 or statusnumber==206:
		cont_typ = content_type(path)
		if cont_typ!=None:
			if "accept-charset" in header_dict:
				response_headlist.append("Content-Type: " + cont_typ + "; charset=utf-8")#; charset=UTF-8")
			else:
				response_headlist.append("Content-Type: " + cont_typ)
		response_headlist.append("Content-Length: " + str(file_length))
		if isfile:
			'''entity_body="<html>\n"
			entity_body+="<head><title>Successfull Response</title></head>\n"
			entity_body+="<body>\n"
			entity_body+="<p>"+file_content+"</p>\n"
			entity_body+="</body>\n"
			entity_body+="</html>"'''
			#entity_body=file_content
			pass
			
		elif isdirectory:
			entity_body="<html>\n"
			entity_body+="<head><title>Listing of the directory</title></head>\n"
			entity_body+="<body><ul>\n"
			for entity in dir_list:	
				entity_body+="<a href=\""+path+"/"+entity+"\"><li>"+entity+"</li></a>\n"
				print("<a href=\"./"+entity+"\"><li>"+entity+"</li></a>\n")
			entity_body+="</ul>\n"
			entity_body+="<p>Listed are all the files and sub-directories in the requested directory.</p>\n"
			entity_body+="</body></html>"
			entity_body=entity_body.encode()
	else:
		entity_body = error_message(statusnumber)
		entity_body=entity_body.encode()

	entity_headers=''
	for r in response_headlist:
		entity_headers+=r+"\n"
	entity_headers+="\n"

	#print(entity_body)
	#print(entity_headers)

	entity_headers=entity_headers.encode()
				
	response = entity_headers + entity_body

	clientsocket.send(response)
	clientsocket.close()

'''def post_method(clientsocket, header_list, data, path):
	response_headlist=deque() #stores response headers
	response_message=''  #stores the message to be sent from server
	header_dict={} #stores the request headers with its content
	display_headers='' #stores the complete response to be sent
	statusnumber=200 #stores the status code (let default be 200)
	isdirectory = 0
	isfile = 0
	
	if data="":
		statusnumber=400
	else:
		path = '''
		
def delete_method(clientsocket, path, header_list):
	response_headlist=deque() #stores response headers
	response_message=''  #stores the message to be sent from server
	header_dict={} #stores the request headers with its content
	display_headers='' #stores the complete response to be sent
	statusnumber=200 #stores the status code (let default be 200)
	isdirectory = 0
	isfile = 0
	
	for header in header_list: #extracts each headers and its value
		temp=header.split(':')
		header_dict[temp[0]] = temp[1]

	if os.path.exists(abs_path):
		if os.access(abs_path, os.R_OK) and os.access(abs_path, os.W_OK):
			if os.path.isfile(abs_path):
				os.remove(abs_path)
			elif os.path.isdir(abs_path):
				os.rmdir(abs_path)
		else:
			statusnumber=403
	else:
		statusnumber=400
		
	for header in header_dict:
		if header.lower()=="host":
			response_headlist.append("Date: " + getdatetime())
	
		elif header.lower()=='user-agent':
			response_headlist.append("Server: Exite/0.1 Ubuntu")
		elif header.lower()=='authorization' and statusnumber==200:
			pass
		elif header.lower()=="content-md5" and statusnumber==200:
			pass
		else:
			continue
	
	response_headlist.appendleft(status_code(statusnumber))

	entity_headers=''
	for r in response_headlist:
		entity_headers+=r+"\n"
	entity_headers+="\n"

	
	if statusnumber==200:
		entity_body = "<html>\n"
		entity_body+="<head><title>Deleted</title></head>\n"
		entity_body+="<body><p>The requested entity has been deleted.</p></body>\n"
		entity_body+="</html>\n"
						
		response = entity_headers + entity_body
	else:
		response = entity_headers
		
	clientsocket.send(response.encode())
	clientsocket.close()
		
		
#first function called to accept the headers from client and checks the method requested
def client_request(clientsocket, address):
	
	message = clientsocket.recv(4096) #accept the headers
	message = message.decode('utf-8') #decode the input #'utf-8'

	requests = message.split('\r\n\r\n') #get the message string
	entity_header = requests[0]
	entity_data = requests[1]
	
	header_list = entity_header.split('\r\n') #split each header
	
	first_line = header_list[0].split() #gets the first line of message
	
	if len(first_line)==3:

		method = first_line[0] #get the method requested
		path = first_line[1] #get the path requested
		version = first_line[2] #get the version requested
			
		if version=='HTTP/1.1':
			header_list.pop(0) #remove the first line since the elements were analysed
			#if path!='':
			if method == 'GET':
				print(header_list)
				get_method(clientsocket, method, path, header_list) #call get method
				'''elif method == 'PUT':
			elif method == 'POST':
			elif method == 'TRACE':
			elif method == 'DELETE':
			elif method == 'HEAD':
				head_method(clientsocket, path, header_list)'''
			#elif something:
			else:
				#raise 405 Method Not Allowed
				
				'''else:
				date=getdatetime()
				error_message = error_message(400)
				content_length = sys.getsizeof(error_message)
						
				headers=status_code(400)
				headers+="Server: Exite/0.1 Ubuntu\n"
				headers+=date
				headers+="Content-Length: "+str(content_length)+"\n"
				headeres+="Content-Type: text/html; charset=iso-8859-1\n"
				response=headers+error_message
				clientsocket.send(response.encode('utf-8'))
				clientsocket.close()'''
				pass
		
		else:
			
			date=getdatetime()
			
			error_response = error_message(505)
			content_length = sys.getsizeof(error_response)
				
			headers=status_code(505)
			headers+="Server: Exite/0.1 Ubuntu\n"
			headers+=date
			headers+="Content-Length: "+str(content_length)+"\n"
			headeres+="Content-Type: text/html; charset=iso-8859-1\n"
			response=headers+error_response
			clientsocket.send(response.encode('utf-8'))
			clientsocket.close()
	else:
		
		date=getdatetime()
		error_response = error_message(400)
		content_length = sys.getsizeof(error_response)
				
		headers=status_code(400)
		headers+="Server: Exite/0.1 Ubuntu\n"
		headers+=date
		headers+="Content-Length: "+str(content_length)+"\n"
		headeres+="Content-Type: text/html; charset=iso-8859-1\n"
		response=headers+error_response
		clientsocket.send(response.encode('utf-8'))
		clientsocket.close()
			
while True:

	connectionsocket, addr = socket.accept()
	t1 = threading.Thread(target=client_request, args=(connectionsocket, addr))
	t1.start()


