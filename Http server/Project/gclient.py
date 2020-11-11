from socket import *
import sys
from multiprocessing import Pool
import threading


serverip='127.0.0.1'
serverport = 1232

headers = []

###################################################

headers1="GET /index.html HTTP/1.1\r\n"
headers1+=f"Host: {serverip}:{serverport}\r\n"
headers1+="Content-Type: text/html\r\n"
headers1+="User-Agent: Mozilla\r\n"
headers1+="Accept-Language: en-US\r\n"
headers1+="Accept-Encoding: */*\r\n\r\n"
headers1 = bytes(headers1, "utf-8")
message1=headers1

headers.append(message1)

###################################################

headers2="GET / HTTP/1.1\r\n"
headers2+=f"Host: {serverip}:{serverport}\r\n"
headers2+="Content-Type: text/plain\r\n"
headers2+="User-Agent: Mozilla\r\n"
headers2+="Accept-Language: en-US\r\n"
headers2+="Accept-Encoding: */*\r\n\r\n"
headers2 = bytes(headers2, "utf-8")
message2=headers2

headers.append(message2)

###################################################

headers3="GET /index.html HTTP/1.1\r\n"
headers3+=f"Host: {serverip}:{serverport}\r\n"
headers3+="Content-Type: text/html\r\n"
headers3+="User-Agent: Mozilla\r\n"
headers3+="Accept-Language: en-US\r\n"
headers3+="Accept-Encoding: */*\r\n"
headers3+="If-Modified-Since: Sun, 07 Nov 2020 12:00:00\r\n\r\n"
headers3 = bytes(headers3, "utf-8")
message3=headers3

headers.append(message3)

###################################################

headers4="GET /postdata HTTP/1.1\r\n"
headers4+=f"Host: {serverip}:{serverport}\r\n"
headers4+="User-Agent: Mozilla\r\n"
headers4+="Accept-Language: en-US\r\n"
headers4+="Accept-Encoding: */*\r\n\r\n"
headers4 = bytes(headers4, "utf-8")
message4=headers4

headers.append(message4)

###################################################

headers5="GET /abc HTTP/1.1\r\n"
headers5+=f"Host: {serverip}:{serverport}\r\n"
headers5+="User-Agent: Mozilla\r\n"
headers5+="Accept-Language: en-US\r\n"
headers5+="Accept-Encoding: */*\r\n\r\n"
headers5 = bytes(headers5, "utf-8")
message5=headers5

headers.append(message5)

###################################################

headers6="GET /111803052_staticrouting.tar.xz HTTP/1.1\r\n"
headers6+=f"Host: {serverip}:{serverport}\r\n"
headers6+="User-Agent: Mozilla\r\n"
headers6+="Accept-Language: en-US\r\n"
headers6+="Accept-Encoding: */*\r\n\r\n"
headers6 = bytes(headers6, "utf-8")
message6=headers6

headers.append(message6)

###################################################

headers7="GET /abc/abc.txt HTTP/1.1\r\n"
headers7+=f"Host: {serverip}:{serverport}\r\n"
headers7+="User-Agent: Mozilla\r\n"
headers7+="Accept-Language: en-US\r\n"
headers7+="Accept-Encoding: */*\r\n\r\n"
headers7 = bytes(headers7, "utf-8")
message7=headers7

headers.append(message7)

###################################################

headers8="GET /locked HTTP/1.1\r\n"
headers8+=f"Host: {serverip}:{serverport}\r\n"
headers8+="User-Agent: Mozilla\r\n"
headers8+="Accept-Language: en-US\r\n"
headers8+="Accept-Encoding: */*\r\n\r\n"
headers8 = bytes(headers8, "utf-8")
message8=headers8

headers.append(message8)

###################################################

headers9="GET /postdata/Screenshot from 2020-11-01 14-42-56.png HTTP/1.1\r\n"
headers9+=f"Host: {serverip}:{serverport}\r\n"
headers9+="Content-Type: image/png\r\n"
headers9+="User-Agent: Mozilla\r\n"
headers9+="Accept-Language: en-US\r\n"
headers9+="Accept-Encoding: */*\r\n"
headers9+="If-Modified-Since: Sun, 07 Nov 2020 12:00:00\r\n\r\n"
headers9 = bytes(headers9, "utf-8")
message9=headers9

headers.append(message9)

###################################################

headers10="GET /postdata/Screenshot from 2020-11-01 14-42-56.png HTTP/1.1\r\n"
headers10+=f"Host: {serverip}:{serverport}\r\n"
headers10+="Content-Type: image/png\r\n"
headers10+="User-Agent: Mozilla\r\n"
headers10+="Accept-Language: en-US\r\n"
headers10+="Accept-Encoding: */*\r\n"
headers10+="If-UnModified-Since: Sat, 07 Nov 2020 12:00:00\r\n\r\n"
headers10 = bytes(headers10, "utf-8")
message10=headers10

headers.append(message10)

###################################################

headers11="GET /postdata/trail.html HTTP/1.1\r\n"
headers11+=f"Host: {serverip}:{serverport}\r\n"
headers11+="Content-Type: text/html\r\n"
headers11+="User-Agent: Mozilla\r\n"
headers11+="Accept-Language: en-US\r\n"
headers11+="Accept-Encoding: */*\r\n"
headers11+="Range: bytes=50-100\r\n\r\n"
headers11 = bytes(headers11, "utf-8")
message11=headers11

headers.append(message11)

###################################################

headers12="GET /postdata/trail.html HTTP/1.1\r\n"
headers12+=f"Host: {serverip}:{serverport}\r\n"
headers12+="Content-Type: text/html\r\n"
headers12+="User-Agent: Mozilla\r\n"
headers12+="Accept-Language: en-US\r\n"
headers12+="Accept-Encoding: */*\r\n"
headers12+="Range: bytes=50-100\r\n"
headers12+="If-Range: Sat, 07 Nov 2020 12:00:00\r\n\r\n"
headers12 = bytes(headers12, "utf-8") 
message12=headers12

headers.append(message12)

###################################################

headers13="GET /postdata/trail.html HTTP/1.1\r\n"
headers13+=f"Host: {serverip}:{serverport}\r\n"
headers13+="Content-Type: text/html\r\n"
headers13+="User-Agent: Mozilla\r\n"
headers13+="Accept-Language: en-US\r\n"
headers13+="Accept-Encoding: */*\r\n"
headers13+="Range: bytes=50-100\r\n"
headers13+="If-UnModified-Since: Sun, 08 Nov 2020 12:00:00\r\n\r\n"
headers13 = bytes(headers13, "utf-8") 
message13=headers13

headers.append(message13)

###################################################

headers14="GET /trail.html HTTP/1.1\r\n"
headers14+=f"Host: {serverip}:{serverport}\r\n"
headers14+="Content-Type: text/html\r\n"
headers14+="User-Agent: Mozilla\r\n"
headers14+="Accept-Language: en-US\r\n"
headers14+="Accept-Encoding: */*\r\n"
headers14+="Range: bytes=50-100\r\n"
headers14+="If-Modified-Since: Sun, 08 Nov 2020 12:00:00\r\n\r\n"
headers14 = bytes(headers14, "utf-8") 
message14=headers14

headers.append(message14)

###################################################

headers15="HEAD /trail.html HTTP/1.1\r\n"
headers15+=f"Host: {serverip}:{serverport}\r\n"
headers15+="Content-Type: text/html\r\n"
headers15+="User-Agent: Mozilla\r\n"
headers15+="Accept-Language: en-US\r\n"
headers15+="Accept-Encoding: */*\r\n"
headers15+="Range: bytes=50-100\r\n"
headers15+="If-Modified-Since: Sun, 08 Nov 2020 12:00:00\r\n\r\n"
headers15 = bytes(headers15, "utf-8") 
message15=headers15

headers.append(message15)

###################################################

headers16="HEAD /trail.html HTTP/1.0\r\n"
headers16+=f"Host: {serverip}:{serverport}\r\n"
headers16+="Content-Type: text/html\r\n"
headers16+="User-Agent: Mozilla\r\n"
headers16+="Accept-Language: en-US\r\n"
headers16+="Accept-Encoding: */*\r\n"
headers16+="Range: bytes=50-100\r\n"
headers16+="If-Modified-Since: Sun, 08 Nov 2020 12:00:00\r\n\r\n"
headers16 = bytes(headers16, "utf-8") 
message16=headers16

headers.append(message16)

###################################################

headers17="GET /644196874.pdf HTTP/1.1\r\n"
headers17+=f"Host: {serverip}:{serverport}\r\n"
headers17+="Content-Type: application/pdf\r\n"
headers17+="User-Agent: Mozilla\r\n"
headers17+="Accept-Language: en-US\r\n"
headers17+="Accept-Encoding: */*\r\n"
headers17+="If-UnModified-Since: Sun, 08 Nov 2020 12:00:00\r\n\r\n"
headers17 = bytes(headers17, "utf-8") 
message17=headers17

headers.append(message17)

###################################################

headers18="GET /Suits Opening .mp3 HTTP/1.1\r\n"
headers18+=f"Host: {serverip}:{serverport}\r\n"
headers18+="Content-Type: audio/mpeg\r\n"
headers18+="User-Agent: Mozilla\r\n"
headers18+="Accept-Language: en-US\r\n"
headers18+="Accept-Encoding: */*\r\n\r\n"
headers18 = bytes(headers18, "utf-8") 
message18=headers18

headers.append(message18)

###################################################

headers19="HEAD /Suits Opening .mp3 HTTP/1.1\r\n"
headers19+=f"Host: {serverip}:{serverport}\r\n"
headers19+="Content-Type: audio/mpeg\r\n"
headers19+="User-Agent: Mozilla\r\n"
headers19+="Accept-Language: en-US\r\n"
headers19+="Accept-Encoding: */*\r\n\r\n"
headers19 = bytes(headers19, "utf-8") 
message19=headers19

headers.append(message19)

###################################################

headers20="HEAD /trail.html HTTP/1.1\r\n"
headers20+=f"Host: {serverip}:{serverport}\r\n"
headers20+="Content-Type: text/html\r\n"
headers20+="User-Agent: Mozilla\r\n"
headers20+="Accept-Language: en-US\r\n"
headers20+="Accept-Encoding: */*\r\n\r\n"
headers20 = bytes(headers20, "utf-8") 
message20=headers20

headers.append(message20)

###################################################

fd1 = open("/home/shubh/Documents/interview.odt", 'rb')
d1 = fd1.read()

body1 = b'-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="fname"\r\n\r\nJohn\r\n-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="lname"\r\n\r\nDoe\r\n-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="myfile"; filename="interview.odt"\r\nContent-Type: application/vnd.oasis.opendocument.text\r\n\r\n' + d1 + b'\r\n' + b'-----------------------------133100775917425215711097468907--\r\n'

l1 = len(body1)

headers21="POST /form.html HTTP/1.1\r\n"
headers21+=f"Host: {serverip}:{serverport}\r\n"
headers21+="Content-Type: multipart/form-data; boundry=-----------------------------133100775917425215711097468907\r\n"
headers21+="User-Agent: Mozilla\r\n"
headers21+="Accept-Language: en-US\r\n"
headers21+=f"Content-Length: {l1}\r\n"
headers21+="Accept-Charset: utf-8\r\n"
headers21+="Accept-Encoding: */*\r\n\r\n"
headers21 = bytes(headers21, "utf-8") 
message21 = headers21+body1

headers.append(message21)

###################################################

body2 = b'-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="fname"\r\n\r\nJohn\r\n-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="lname"\r\n\r\nDoe\r\n-----------------------------133100775917425215711097468907--\r\n'


l2 = len(body2)

headers22="POST /form.html HTTP/1.1\r\n"
headers22+=f"Host: {serverip}:{serverport}\r\n"
headers22+="Content-Type: multipart/form-data; boundry=-----------------------------133100775917425215711097468907\r\n"
headers22+="User-Agent: Mozilla\r\n"
headers22+="Accept-Language: en-US\r\n"
headers22+=f"Content-Length: {l2}\r\n"
headers22+="Accept-Charset: utf-8\r\n"
headers22+="Accept-Encoding: */*\r\n\r\n"
headers22 = bytes(headers22, "utf-8") 
message22 = headers22+body2

headers.append(message22)

###################################################

body3 = 'fname=Shubh&lname=Gohil'


l3 = len(body3)

headers23="POST /form.html HTTP/1.1\r\n"
headers23+=f"Host: {serverip}:{serverport}\r\n"
headers23+="Content-Type: application/x-www-form-urlencoded\r\n"
headers23+="User-Agent: Mozilla\r\n"
headers23+="Accept-Language: en-US\r\n"
headers23+=f"Content-Length: {l3}\r\n"
headers23+="Accept-Charset: utf-8\r\n"
headers23+="Accept-Encoding: */*\r\n\r\n"
#headers23 = bytes(headers23, "utf-8") 
message23 = headers23+body3
message23 = bytes(message23, "utf-8") 
headers.append(message23)

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

fd2 = open("postdata/trail.html", 'r')
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
headers.append(message25)

##########################################

fd3 = open("postdata/Simplication of cfg - 1.odt", 'rb')
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

##########################################

fd4 = open("postdata/Nuance.odt", 'rb')
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

##########################################

fd5 = open("postdata/111803052_Shubh_Gohil_CaseStudy_2&3.ods", 'rb')
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

headers.append(message28)

##########################################

fd6 = open("Suits Opening .mp3", 'rb')
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

headers.append(message29)

##########################################


headers30="DELETE /t1.txt HTTP/1.1\r\n"
headers30+=f"Host: {serverip}:{serverport}\r\n"
headers30+="Content-Type: text/plain\r\n"
headers30+="User-Agent: Mozilla\r\n\r\n"
headers30 = bytes(headers30, "utf-8")
message30=headers30

headers.append(message30)

########################################

headers31="DELETE /asf HTTP/1.1\r\n"
headers31+=f"Host: {serverip}:{serverport}\r\n"
headers31+="Content-Type: text/plain\r\n"
headers31+="User-Agent: Mozilla\r\n\r\n"
headers31 = bytes(headers31, "utf-8")
message31=headers31

headers.append(message31)

########################################

headers32="DELETE /locked HTTP/1.1\r\n"
headers32+=f"Host: {serverip}:{serverport}\r\n"
headers32+="Content-Type: text/plain\r\n"
headers32+="User-Agent: Mozilla\r\n\r\n"
headers32 = bytes(headers32, "utf-8")
message32=headers32

headers.append(message32)

########################################

headers33="GET /style.css HTTP/1.1\r\n"
headers33+=f"Host: {serverip}:{serverport}\r\n"
headers33+="Content-Type: text/css\r\n"
headers33+="User-Agent: Mozilla\r\n"
headers33+="Accept-Language: en-US\r\n"
headers33+="Accept-Encoding: */*\r\n\r\n"
headers33 = bytes(headers33, "utf-8")
message33=headers33

headers.append(message33)

###################################################

headers34="GET /main.js HTTP/1.1\r\n"
headers34+=f"Host: {serverip}:{serverport}\r\n"
headers34+="Content-Type: application/javascript\r\n"
headers34+="User-Agent: Mozilla\r\n"
headers34+="Accept-Language: en-US\r\n"
headers34+="Accept-Encoding: */*\r\n\r\n"
headers34 = bytes(headers34, "utf-8")
message34=headers34

headers.append(message34)

###################################################

headers35="GET /VID-20201105-WA0002.mp4 HTTP/1.1\r\n"
headers35+=f"Host: {serverip}:{serverport}\r\n"
headers35+="Content-Type: video/mp4\r\n"
headers35+="User-Agent: Mozilla\r\n"
headers35+="Accept-Language: en-US\r\n"
headers35+="Accept-Encoding: */*\r\n\r\n"
headers35 = bytes(headers35, "utf-8")
message35=headers35

headers.append(message35)

###################################################

headers36="GET /IMG-20181116-WA0000.jpg HTTP/1.1\r\n"
headers36+=f"Host: {serverip}:{serverport}\r\n"
headers36+="Content-Type: image/jpg\r\n"
headers36+="User-Agent: Mozilla\r\n"
headers36+="Accept-Language: en-US\r\n"
headers36+="Accept-Encoding: */*\r\n\r\n"
headers36 = bytes(headers36, "utf-8")
message36=headers36

headers.append(message36)

###################################################

headers37="GET /COI PRESENTATION-1.docx HTTP/1.1\r\n"
headers37+=f"Host: {serverip}:{serverport}\r\n"
headers37+="Content-Type: application/msword\r\n"
headers37+="User-Agent: Mozilla\r\n"
headers37+="Accept-Language: en-US\r\n"
headers37+="Accept-Encoding: */*\r\n\r\n"
headers37 = bytes(headers37, "utf-8")
message37=headers37

headers.append(message37)

###################################################

headers37="GET /COI PRESENTATION-1.docx HTTP/1.1\r\n"
headers37+=f"Host: {serverip}:{serverport}\r\n"
headers37+="Content-Type: application/msword\r\n"
headers37+="User-Agent: Mozilla\r\n"
headers37+="Accept-Language: en-US\r\n"
headers37+="Cookie: yjfjy\r\n"
headers37+="Accept-Encoding: */*\r\n\r\n"
headers37 = bytes(headers37, "utf-8")
message37=headers37

headers.append(message37)

###################################################

fd7 = open("VID-20201105-WA0002.mp4", 'rb')
d2 = fd7.read()

body9 = b'-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="fname"\r\n\r\nJohn\r\n-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="lname"\r\n\r\nDoe\r\n-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="myfile"; filename="interview.odt"\r\nContent-Type: video/mp4\r\n\r\n' + d2 + b'\r\n' + b'-----------------------------133100775917425215711097468907--\r\n'

l9 = len(body9)

headers38="POST /VID-20201105-WA0002.mp4 HTTP/1.1\r\n"
headers38+=f"Host: {serverip}:{serverport}\r\n"
headers38+="Content-Type: multipart/form-data; boundry=-----------------------------133100775917425215711097468907\r\n"
headers38+="User-Agent: Mozilla\r\n"
headers38+="Accept-Language: en-US\r\n"
headers38+=f"Content-Length: {l1}\r\n"
headers38+="Accept-Charset: utf-8\r\n"
headers38+="Accept-Encoding: */*\r\n\r\n"
headers38 = bytes(headers38, "utf-8") 
message38 = headers38+body9

headers.append(message38)

###################################################

fd8 = open("VID-20201105-WA0002.mp4", 'rb')
d3 = fd8.read()

body10 = b'-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="fname"\r\n\r\nApple\r\n-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="fname"\r\n\r\nOrange\r\n-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data;name="fname"\r\n\r\nGrapes\r\n-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="fname"\r\n\r\nCustard Apple\r\n-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data;   name="lname"\r\n\r\nMango\r\n-----------------------------133100775917425215711097468907\r\nContent-Disposition: form-data; name="myfile"; filename="interview.odt"\r\nContent-Type: video/mp4\r\n\r\n' + d3 + b'\r\n' + b'-----------------------------133100775917425215711097468907--\r\n'

l10 = len(body10)

headers39="POST /VID-20201105-WA0002.mp4 HTTP/1.1\r\n"
headers39+=f"Host: {serverip}:{serverport}\r\n"
headers39+="Content-Type: multipart/form-data; boundry=-----------------------------133100775917425215711097468907\r\n"
headers39+="User-Agent: Mozilla\r\n"
headers39+="Accept-Language: en-US\r\n"
headers39+=f"Content-Length: {l1}\r\n"
headers39+="Accept-Charset: utf-8\r\n"
headers39+="Accept-Encoding: */*\r\n\r\n"
headers39 = bytes(headers39, "utf-8") 
message39 = headers39+body10

headers.append(message38)

###################################################

body11 = 'fname=Shubh&lname=Gohil'


l11 = len(body11)

headers40="POST /form.html HTTP/1.1\r\n"
headers40+=f"Host: {serverip}:{serverport}\r\n"
headers40+="Content-Type: application/x-www-form-urlencoded\r\n"
headers40+="User-Agent: Mozilla\r\n"
headers40+="Accept-Language: en-US\r\n"
headers40+=f"Content-Length: {l3}\r\n"
headers40+="Accept-Charset: utf-8\r\n"
headers40+="Accept-Encoding: */*\r\n\r\n"
#headers23 = bytes(headers23, "utf-8") 
message40 = headers40+body11
message40 = bytes(message40, "utf-8") 
headers.append(message40)

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

def send(message):
	
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

'''
clientsocket = socket(AF_INET, SOCK_STREAM)
clientsocket.connect((serverip, serverport))

clientsocket.send(message37)
ans = clientsocket.recv(8192)
#print("Response for request from ", clientsocket)
try:
	print(ans.decode('utf-8'))
except:
	print(ans)
		
print()
clientsocket.close()	
'''


