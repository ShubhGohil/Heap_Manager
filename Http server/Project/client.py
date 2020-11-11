from socket import *
import sys
serverip='127.0.0.1'
serverport = 1233

socket = socket(AF_INET, SOCK_STREAM)
socket.connect((serverip, serverport))
fd = open("postdata/Screenshot from 2020-11-01 14-42-56.png", "rb")
body = fd.read()
fd.close()


headers="PUT /postdata/Screenshot from 2020-11-01 14-42-56.png HTTP/1.1\r\n"
headers+="Host: Me\r\n"
headers+="Content-Type: text/plain\r\n"
headers+="User-Agent: Mozilla\r\n"
headers+="Content-Length: " + str(len(body)) + '\r\n\r\n'
headers = bytes(headers, "utf-8")
message=headers+body+ b'\r\n'


socket.send(message)
ans = socket.recv(1024)
print(ans.decode())


