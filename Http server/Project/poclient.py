from socket import *
import sys
import threading
serverip='127.0.0.1'
serverport = 1232


socket = socket(AF_INET, SOCK_STREAM)
socket.connect((serverip, serverport))

###################################################

'''fd = open("/home/shubh/Documents/interview.odt", 'rb')
d = fd.read()

body = b'-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="fname"\r\n\r\nJohn\r\n-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="lname"\r\n\r\nDoe\r\n-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="myfile"; filename="interview.odt"\r\nContent-Type: application/vnd.oasis.opendocument.text\r\n\r\n' + d + b'\r\n' + b'-----------------------------133100775917425215711097468907--\r\n'

l = len(body)

headers="POST /form.html HTTP/1.1\r\n"
headers+=f"Host: {serverip}:{serverport}\r\n"
headers+="Content-Type: multipart/form-data; boundry=-----------------------------133100775917425215711097468907\r\n"
headers+="User-Agent: Mozilla\r\n"
headers+="Accept-Language: en-US\r\n"
headers+=f"Content-Length: {l}\r\n"
headers+="Accept-Charset: utf-8\r\n"
headers+="Accept-Encoding: */*\r\n\r\n"
'''

###################################################

'''body = b'-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="fname"\r\n\r\nJohn\r\n-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="lname"\r\n\r\nDoe\r\n-----------------------------133100775917425215711097468907--\r\n'


l = len(body)

headers="POST /form.html HTTP/1.1\r\n"
headers+=f"Host: {serverip}:{serverport}\r\n"
headers+="Content-Type: multipart/form-data; boundry=-----------------------------133100775917425215711097468907\r\n"
headers+="User-Agent: Mozilla\r\n"
headers+="Accept-Language: en-US\r\n"
headers+=f"Content-Length: {l}\r\n"
headers+="Accept-Charset: utf-8\r\n"
headers+="Accept-Encoding: */*\r\n\r\n"
'''
###################################################

'''body = 'fname=Shubh&lname=Gohil'


l = len(body)

headers="POST /form.html HTTP/1.1\r\n"
headers+=f"Host: {serverip}:{serverport}\r\n"
headers+="Content-Type: application/x-www-form-urlencoded\r\n"
headers+="User-Agent: Mozilla\r\n"
headers+="Accept-Language: en-US\r\n"
headers+=f"Content-Length: {l}\r\n"
headers+="Accept-Charset: utf-8\r\n"
headers+="Accept-Encoding: */*\r\n\r\n"
'''
###################################################


headers = bytes(headers, "utf-8")
message=headers+body
socket.send(message)
ans = socket.recv(8192)
print(ans)
