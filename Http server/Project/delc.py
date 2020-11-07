from socket import *
import sys
serverip='127.0.0.1'
serverport = 1233

socket = socket(AF_INET, SOCK_STREAM)
socket.connect((serverip, serverport))


headers="DELETE /putdata/sbc.odt HTTP/1.1\r\n"
headers+="Host: Me\r\n"
headers+="Content-Type: text/plain\r\n"
headers+="User-Agent: Mozilla\r\n\r\n"
headers = bytes(headers, "utf-8")
message=headers


socket.send(message)
ans = socket.recv(1024)
print(ans.decode())


