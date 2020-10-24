from socket import *
import sys
import threading
import os
import time
from collections import deque
import datetime
from urllib.parse import *
import random
import string
import binascii

month = { 'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12 }

file_extension = {'html':'text/html', 'txt':'text/plain', 'png':'image/png', 'gif': 'image/gif', 'jpg':'image/jpg', 'ico': 'image/x-icon', 'php':'application/x-www-form-urlencoded', '': 'text/plain', 'jpeg':'image/webp', 'pdf': 'application/pdf', 'js': 'application/javascript', 'css': 'text/css', 'mp3' : 'audio/mpeg', 'mp4': 'video/mp4'}

file_type = {'text/html': '.html','text/plain': '.txt', 'image/png': '.png', 'image/gif': '.gif', 'image/jpg': '.jpg','image/x-icon':'.ico', 'image/webp': '.jpeg', 'application/x-www-form-urlencoded':'.php', 'image/jpeg': '.jpeg', 'application/pdf': '.pdf', 'audio/mpeg': '.mp3', 'video/mp4': '.mp4'}

media_type = ["image/png", "image/jpg", "image/x-icon", "image/gif", "audio/mpeg", "image/webp", "application/pdf", "video/mp4"]

'''def server_status():
	state = input()
	if state.lower()=='close':
		serversocket.close()
		sys.exit()
	else:
		pass'''

serverport = 1234 #server port number
serversocket = socket(AF_INET, SOCK_STREAM) #create a socket
serversocket.bind(("127.0.0.1", serverport)) #bind the server with ip and port
serversocket.listen(50) #No. of connectinos allowed to queue

'''s = threading.Thread(target=server_status, args=())
s.start()'''

def resolve(element):
	params = parse_qs(element)
	values = []
	for key in params.values():
		values.append(key[0]+"\n")
	return values, params

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
def error_entitybody(code):
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

def complete_error_response(clientsocket, code):
	date=getdatetime()
	error_response = error_entitybody(code)
	content_length = sys.getsizeof(error_response)
			
	headers=status_code(code)
	headers+="Server: Exite/0.1 Ubuntu\n"
	headers+=date
	headers+="Content-Length: "+str(content_length)+"\n"
	headers+="Content-Type: text/html; charset=utf-8\n"
	response=headers+error_response
	clientsocket.send(response.encode('utf-8'))
	clientsocket.close()
		

#GET
def get_method(clientsocket, address, method, path, header_list):
	response_headlist=deque() #stores response headers
	header_dict={} #stores the request headers with its content
	statusnumber=200 #stores the status code (let default be 200)
	isdirectory = 0
	isfile = 0 
	conditional_get = 0 #condition for if-modified
	size = 0 #bytes of file to be read
	range_head = 0 #flag for range headers
	start, end = 0, 0 #for range headers to determine end and start bytes
	available = 0 #checks if the accept headers file is available
	
	if method=='GET':
		get = 1
	else:
		get = 0
	
	client_ip = address[0]
	request_method_line = header_list.pop(0)
	date = getdatetime()
	
	for header in header_list: #extracts each headers and its value
		if header[0:17].lower()=="if-modified-since":
			header_dict[header[:17].lower()] = header[18:]
		elif header[0:8].lower()=='if-range':
			header_dict[header[:8].lower()] = header[9:]
		elif header[:10].lower()=='user-agent':
			header_dict[header[:10].lower()] = header[11:]
		else:
			temp=header.split(':')
			if temp[0]=="range":
				size = int(temp[1])
			header_dict[temp[0].lower()] = temp[1]	
		
	abs_path = os.getcwd()+path #stores the complete path of requested file or directory

	if 'range' in header_dict.keys():
		if 'if-range' in header_dict.keys():
			if not compare_time_if_modified(abs_path, header_dict['if-range']):
				start = int(header_dict['range'].split('-')[0].replace(' ',''))
				end = int(header_dict['range'].split('-')[1])
				size= end - start + 1
				range_head = 1

		else:
			start = int(header_dict['range'].split('-')[0].replace(' ',''))
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
			print(abs_path)
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
		if header=="host":
			response_headlist.append("Date: " + getdatetime())
	
		#elif header=="Accept": 
		#	accept_type = header_dict[header].split(",")
		#	available = [f_type for f_type in accept_type if f_type in file_type]
		#	print(available)			
		#	response_headers.append("Content-Type: ")
		#	pass
		#else:
		#	statusnumber = 406
		elif header=='user-agent':
			response_headlist.append("Server: Exite/0.1 Ubuntu")
			user_agent = header_dict[header]
				
		elif header=='accept-language':
			if header_dict['accept-language']==' en-US' or header_dict['accept-language'].split(',')[0]==' en-US':
				response_headlist.append("Content-Language: en-US")
			
		elif header=='accept-encoding' and statusnumber==200:
			response_headlist.append("Content-Encoding: identity")
				
		elif header=="content-md5" and statusnumber==200:
			pass
			
		elif header=='if-modified-since' and statusnumber==200:
			conditional_get = compare_time_if_modified(abs_path, header_dict[header])
			if conditional_get:
				response_headlist.append("Last-Modified: " + getdatetime(abs_path))
			else:
				statusnumber = 304
					
		elif header=='if-unmodified-since' and statusnumber==200:
			conditional_get = compare_time_if_modified(abs_path, header_dict[header])
			if not conditional_get:
				response_headlist.append("Last-Modified: " + getdatetime(abs_path))
			else:
				statusnumber = 304
		
		else:
			continue
		
	if 'cookie' not in header_dict:
		cookie = random.choice(string.ascii_letters)
		cookie += random.choice(string.ascii_letters)
		cookie += str(random.randint(0,9))
		cookie += str(random.randint(0,9))		
		cookie += str(random.randint(0,9))
		response_headlist.append("Set-Cookie : " + cookie)
		#store the cookie in the file cookie.txt and it is imp
		
	response_headlist.appendleft(status_code(statusnumber))
	
	if get:
		if statusnumber==200 or statusnumber==206:
			cont_typ = content_type(path)
			if cont_typ!=None:
				if "accept-charset" in header_dict:
					response_headlist.append("Content-Type: " + cont_typ + "; charset=utf-8")#; charset=UTF-8")
				else:
					response_headlist.append("Content-Type: " + cont_typ)
			response_headlist.append("Content-Length: " + str(file_length))
				
			if isdirectory:
				entity_body="<html>\n"
				entity_body+="<head><title>Listing of the directory</title></head>\n"
				entity_body+="<body><ul>\n"
				for entity in dir_list:	
					entity_body+="<a href=\""+path+"/"+entity+"\"><li>"+entity+"</li></a>\n"
				entity_body+="</ul>\n"
				entity_body+="<p>Listed are all the files and sub-directories in the requested directory.</p>\n"	
				entity_body+="</body></html>"
				entity_body=entity_body.encode()
		else:
			entity_body = error_entitybody(statusnumber)
			entity_body=entity_body.encode()
	
	response_code = str(statusnumber)
	
	try:
		log_entry = client_ip + ", [" + date + "], " + request_method_line + ", " + response_code + ", " + user_agent + "\n-----------------------------------------" +"\n\n"
#		if not os.path.exits(os.getcwd()+"access.log")
		
		fd = open("access.log", "a")
		fd.write(log_entry)
		fd.close()
	except:
		pass
		
	entity_headers=''
	for r in response_headlist:
		entity_headers+=r+"\n"
	entity_headers+="\n"
	
	entity_headers=entity_headers.encode()				

	if get:
		response = entity_headers + entity_body
	else:
		response = entity_headers
		
	clientsocket.send(response)
	clientsocket.close()



#POST
def post_method(clientsocket, address, header_list, path, data=""):
	response_headlist=deque() #stores response headers
	value=deque()
	response_message=''  #stores the message to be sent from server
	header_dict={} #stores the request headers with its content
	statusnumber=204 #stores the status code (let default be 200)
	content_length = 0
	entity_headers="" #stores the complete response to be sent
	log_data = ''

	client_ip = address[0]
	request_method_line = header_list.pop(0)
	date = getdatetime()


	for header in header_list: #extracts each headers and its value
		temp=header.split(':')
		header_dict[temp[0].lower()] = temp[1]

	#if a file is posted 
	if "multipart/form-data" in header_dict["content-type"]:
		value_type = header_dict["content-type"].split(';')
		boundry = value_type[1].split('=')[1]
		all_data = data.split("--"+boundry)

		for individual in all_data:
			try:
				if "Content-Disposition" in individual:
					if 'filename' in individual:
						log_data += individual.split('\r\n\r\n', 1)[0] + '\n\n'
						log_data += "Location: " + os.getcwd()
					else:
						log_data += individual
					
				details = individual.split("\r\n\r\n", 1)
				file_data = details[1]
				#filename = details[0]
				if "Content-Type" in details[0]:
					content_type = details[0].split('\r\n')[-1]
					filetype = content_type.split(':')[-1].replace(" ", "")
					print(filetype)
					extract_filename = details[0].split('\r\n')[-2].split(';')[-1]
					filename = extract_filename.split('=')[-1].replace('\"', "")
					print(filename)
					
				value.append(details[1]) 
				
				if file_type in media_type: 
					try:
						fd = open(filename, 'wb')
						fd.write(file_data)
						fd.close()
					except:
						pass
				else:
					try:
						fd = open(filename, 'w')
						fd.write(file_data)
						fd.close()
					except:
						pass
					
			except:
				pass

	#if simple values are passed
	elif "application/x-www-form-urlencoded" in header_dict["content-type"]:
		value, log_data = resolve(data)
		content_type = "text/plain"

		
	entity_headers+=status_code(statusnumber)+"\n"
	entity_headers+="Date: "+getdatetime()+"\n"				
	entity_headers+=content_type+"\n"		
	entity_headers+="Server: Exite/0.1 Ubuntu\n\n"

	
	if statusnumber!=204:
		response = entity_headers + error_entitybody(statusnumber)
	else:
		response = entity_headers

	response_code = str(statusnumber)

	try:
		log_entry = client_ip + ", [" + date + "], " + request_method_line + ", " + response_code + ", \n" + "The data of the form is:\n" + str(log_data) + "\n------------------------------------------" +"\n\n"

		print(log_entry)
		fd = open("access.log", "a")
		fd.write(log_entry)
		fd.close()
	
	except :
		pass
			
	clientsocket.send(response.encode())
	clientsocket.close()


def put_method(clientsocket, address, header_list, path, data=""):
	response_headlist=deque() #stores response headers
	header_dict={} #stores the request headers with its content
	statusnumber=204 #stores the status code (let default be 200)
	content_length = 0
	entity_headers="" #stores the complete response to be sent
	log_data = ''
	
	client_ip = address[0]
	request_method_line = header_list.pop(0)
	date = getdatetime()
	log_data = data

	print(data)

	for header in header_list: #extracts each headers and its value
		temp=header.split(':')
		header_dict[temp[0].lower()] = temp[1]
	
	abs_path = os.getcwd() + path
		
	if os.path.exists(abs_path):
		if os.access(abs_path, os.R_OK) and os.access(abs_path, os.W_OK):
		
			try:
				fd = open(path[1:], "a")
				fd.write(data)
				fd.close()
				statusnumber = 200
				
			except:
				statusnumber=500
	else:
		try:
			fd = open(path[1:], "w")
			fd.write(data)
			fd.close()
			statusnumber = 201
			
		except:
			statusnumber = 500
			
	entity_headers = status_code(statusnumber) + '\r\n'
	entity_headers += "Date: " + getdatetime() + '\r\n'
	entity_headers += "Content-Location: " + path + '\r\n\r\n'
	
	if statusnumber == 200:
		entity_body = "<html>\r\n<head><title>Successfull</title></head>\r\n<body><p>The data has been saved.</p>\r\n</body>\r\n</html>"
		response = entity_headers + entity_body

	elif statusnumber == 500:
		entity_body = error_message(statusnumber)
		response = entity_headers + entity_body
	else:
		response = entity_headers
	
	response_code = str(statusnumber)
	
	fd = open("access.log", "a")
	log_entry = client_ip + ", [" + date + "], " + request_method_line + ", " + response_code + ", \n" + "The data of the form is:\n" + str(log_data) + "\n------------------------------------------" +"\n\n"
	fd.write(log_entry)
	fd.close()
	
	#print(response)
	
	clientsocket.send(response.encode())
	clientsocket.close()

#DELETE
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

	try:
		message = clientsocket.recv(4096) #accept the headers
		message = message.decode()#'utf-8') #decode the input #'utf-8'
		requests = message.split('\r\n\r\n', 1)
		entity_header = requests[0]
		entity_data = requests[1]

	except:
		message = message.decode(errors = 'ignore')
		requests = message.split('\r\n\r\n', 1)
		
		#requests = message.split('\r\n\r\n') #get the message string
			
		entity_header = requests[0]
		#entity_header = entity_header.decode()
		entity_data = requests[1]
	
	header_list = entity_header.split('\r\n')
	#header_list = entity_header.split('\r\n') #split each header
		
	first_line = header_list[0].split() #gets the first line of message
		
	
	if len(first_line)==3:

		method = first_line[0] #get the method requested
		path = first_line[1] #get the path requested
		version = first_line[2] #get the version requested
			
		if version=='HTTP/1.1':
			#header_list.pop(0) #remove the first line since the elements were analysed
			#if path!='':
			if method == 'GET':
				get_method(clientsocket, address, method, path, header_list) #call get method
				
			elif method == 'POST':
				post_method(clientsocket, address, header_list, path, entity_data) #call post method
						
			elif method == 'PUT':
				put_method(clientsocket, address, header_list, path, entity_data) #call put method
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
			complete_error_response(clientsocket, 505)
	else:
		complete_error_response(clientsocket, 400)
			
while True:

	connectionsocket, addr = serversocket.accept()
	t1 = threading.Thread(target=client_request, args=(connectionsocket, addr))
	t1.start()
	

#https://github.com/roopi7760/WebServer/blob/master/Server.py
#https://github.com/sm8799/HTTP-Web-Server/blob/master/webserver.py
