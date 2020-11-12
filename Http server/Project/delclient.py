from socket import *
import sys
serverip='127.0.0.1'
serverport = 1232

socket = socket(AF_INET, SOCK_STREAM)
socket.connect((serverip, serverport))

########################################

'''headers="DELETE /t1.txt HTTP/1.1\r\n"
headers+=f"Host: {serverip}:{serverport}\r\n"
headers+="Content-Type: text/plain\r\n"
headers+="User-Agent: Mozilla\r\n\r\n"
headers = bytes(headers, "utf-8")
message=headers
'''

########################################

'''headers="DELETE /asf HTTP/1.1\r\n"
headers+=f"Host: {serverip}:{serverport}\r\n"
headers+="Content-Type: text/plain\r\n"
headers+="User-Agent: Mozilla\r\n\r\n"
headers = bytes(headers, "utf-8")
message=headers
'''

########################################

'''headers="DELETE /locked HTTP/1.1\r\n"
headers+=f"Host: {serverip}:{serverport}\r\n"
headers+="Content-Type: text/plain\r\n"
headers+="User-Agent: Mozilla\r\n\r\n"
headers = bytes(headers, "utf-8")
message=headers
'''

########################################

'''headers="DELETE /t3.txt HTTP/1.1\r\n"
headers+=f"Host: {serverip}:{serverport}\r\n"
headers+="Content-Type: text/plain\r\n"
headers+="Authorization: 1234\r\n"
headers+="User-Agent: Mozilla\r\n\r\n"
headers = bytes(headers, "utf-8")
message=headers
'''

########################################

headers="DELETE /t3.txt HTTP/1.1\r\n"
headers+=f"Host: {serverip}:{serverport}\r\n"
headers+="Content-Type: text/plain\r\n"
headers+="Authorization: 12345678\r\n"
headers+="User-Agent: Mozilla\r\n\r\n"
headers = bytes(headers, "utf-8")
message=headers

########################################

socket.send(message)
ans = socket.recv(1024)
print(ans.decode())


