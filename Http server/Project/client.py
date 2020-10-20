from socket import *
serverip='127.0.0.1'
serverport = 1234

socket = socket(AF_INET, SOCK_STREAM)
socket.connect((serverip, serverport))
message="POST /index.html HTTP/1.1\n"
message+="Host: Me\n"
message+="Content-Type:application/x-www-form-urlencoded\n"
message+="User-Agent:Mozilla\n"
message+="Accept:*/*\n"
message+="If-Modified-Since:Thu, 15 Oct 2021 21:23:34 GMT\n\n"
message+="<html><body><h2>HTML Forms</h2><form><label for=\"fname\">First name:</label><br><input type=\"text\" id=\"fname\" name=\"fname\" value=\"John\"><br><label for=\"lname\">Last name:</label><br><input type=\"text\" id=\"lname\" name=\"lname\" value=\"Doe\"><br><br><input type=\"submit\" value=\"Submit\"></form> </body></html>"


socket.send(message.encode())

