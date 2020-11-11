from socket import *
import sys
from multiprocessing import Pool
import threading

serverip='127.0.0.1'
serverport = 1232
	
clientsocket = socket(AF_INET, SOCK_STREAM)
clientsocket.connect((serverip, serverport))

headers = []
##########################################

headers24="PUT /trail.html HTTP/1.1\r\n"
headers24+=f"Host: {serverip}:{serverport}\r\n"
headers24+="Content-Type: text/html\r\n"
headers24+="User-Agent: Mozilla\r\n"
headers24+="Accept-Language: en-US\r\n"
headers24+="Accept-Encoding: */*\r\n\r\n"
headers24 = bytes(headers24, "utf-8") 
message24=headers24

headers.append(message24)

##########################################

'''fd2 = open("postdata/trail.html", 'r')
body4 = fd2.read()
fd2.close()

l4 = len(body4)

headers25="PUT /trail.html HTTP/1.1\r\n"
headers25+=f"Host: {serverip}:{serverport}\r\n"
headers25+="Content-Type: text/html\r\n"
headers25+="User-Agent: Mozilla\r\n"
headers25+=f"Content-length: {l4}\r\n"
headers25+="Accept-Language: en-US\r\n"
headers25+="Accept-Encoding: */*\r\n\r\n"
#headers25 = bytes(headers25, "utf-8") 
message25=headers25+body4

message25 = bytes(message25, "utf-8")
headers.append(message25)'''

##########################################

'''fd3 = open("postdata/Simplication of cfg - 1.odt", 'rb')
body5 = fd3.read()
fd3.close()

l5 = len(body5)

headers26="PUT /Simplication of cfg - 1.odt HTTP/1.1\r\n"
headers26+=f"Host: {serverip}:{serverport}\r\n"
headers26+="Content-Type: application/vnd.oasis.opendocument.text\r\n"
headers26+=f"Content-length: {l5}\r\n"
headers26+="User-Agent: Mozilla\r\n"
headers26+="Accept-Language: en-US\r\n"
headers26+="Accept-Encoding: */*\r\n\r\n"
headers26 = bytes(headers26, "utf-8") 
message26=headers26+body5

headers.append(message26)
'''
##########################################

'''fd4 = open("postdata/Nuance.odt", 'rb')
body6 = fd4.read()
fd4.close()

l6 = len(body6)

headers27="PUT /Nuance.odt HTTP/1.1\r\n"
headers27+=f"Host: {serverip}:{serverport}\r\n"
headers27+="Content-Type: application/vnd.oasis.opendocument.text\r\n"
headers27+=f"Content-length: {l6}\r\n"
headers27+="User-Agent: Mozilla\r\n"
headers27+="Accept-Language: en-US\r\n"
headers27+="Accept-Encoding: */*\r\n\r\n"
headers27 = bytes(headers27, "utf-8") 
message27=headers27+body6

headers.append(message27)
'''
##########################################

'''fd5 = open("postdata/111803052_Shubh_Gohil_CaseStudy_2&3.ods", 'rb')
body7 = fd5.read()
fd5.close()

l7 = len(body7)

headers28="PUT /111803052_Shubh_Gohil_CaseStudy_2&3.ods HTTP/1.1\r\n"
headers28+=f"Host: {serverip}:{serverport}\r\n"
headers28+="Content-Type: application/vnd.oasis.opendocument.spreadsheet\r\n"
headers28+=f"Content-length: {l7}\r\n"
headers28+="User-Agent: Mozilla\r\n"
headers28+="Accept-Language: en-US\r\n"
headers28+="Accept-Encoding: */*\r\n\r\n"
headers28 = bytes(headers28, "utf-8") 
message28=headers28+body7

headers.append(message28)'''

##########################################

'''fd6 = open("Suits Opening .mp3", 'rb')
body8 = fd6.read()
fd6.close()

l8 = len(body8)

headers29="PUT /Suits Opening .mp3 HTTP/1.1\r\n"
headers29+=f"Host: {serverip}:{serverport}\r\n"
headers29+="Content-Type: audio/mpeg\r\n"
headers29+=f"Content-length: {l8}\r\n"
headers29+="User-Agent: Mozilla\r\n"
headers29+="Accept-Language: en-US\r\n"
headers29+="Accept-Encoding: */*\r\n\r\n"
headers29 = bytes(headers29, "utf-8") 
message29=headers29+body8

headers.append(message29)'''

##########################################

'''clientsocket.send(message.encode())

ans = clientsocket.recv(8192)
print(ans)'''


def send(message):
	serverip='127.0.0.1'
	serverport = 1232
	

	clientsocket = socket(AF_INET, SOCK_STREAM)
	clientsocket.connect((serverip, serverport))

	clientsocket.send(message)
	ans = clientsocket.recv(8192)
	print("Response for request from ", clientsocket)
	try:
		print(ans.decode('utf-8'))
	except:
		print(ans)
		
	print()
	clientsocket.close()	

with Pool(5) as p:
	p.map(send, headers)

