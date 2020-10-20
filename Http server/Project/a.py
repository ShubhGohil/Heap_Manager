import datetime
from urllib.parse import *
import os
import time
import urllib.parse
import sys
#print(os.getcwd())#+'/abc'
#print(os.path.isdir(path))
'''def resolve(element):
	u = urlparse(element)
	element = unquote(u.path)
	if element == '/':
		element = os.getcwd()
	query = parse_qs(u.query)
	return (element, query)
	
a='http://amazon.com/abc/index.html'
element, query=resolve(a) 
print(element, query)'''

month = { 'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12 }

#print(os.access(path, os.X_OK))'''

#if os.access(abs_path, os.W_OK):# and os.access(abs_path, os.W_OK):
#	print("Working")

'''def file_lastmdate(path):
	file_modification_time=os.path.getmtime(path) #provides last modification time from epoch in sec 
	readable_time = time.ctime(file_modification_time) #converts in readable format
	separate = readable_time.split()
	separate[0]+=","
	
	order="02143" #order in which the readable format has to be arranged to get standard internet format
	internet_std_time=''
	
	for i in order:
		internet_std_time = internet_std_time + separate[int(i)] + " "
	internet_std_time+="GMT"
		
	return "Date: " + internet_std_time #Date header
	
def compare_time_if_modified(path, given_time):
	try:
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
	except:
		return "error"

print(file_lastmdate(path))
print(compare_time_if_modified(path, 'Sun, 11 Oct 2020 16:19:55 GMT'))'''

#print(time.ctime())
'''
a=''
a+="<html>"
a+="<head></head>"
a+="<body>Hi there</body>"
a+="</html>"
print(sys.getsizeof(a))'''


abs_path=os.getcwd()+'/'

#print("If-Modified-Since".lower())
'''asd='/'
print(asd.split('/'))'''

query1 = "http://www.example.org/default.html?ct=32&op=92&item=98"
query2 = "Name=Shubh%25Gohil&College=COEP"
query3 = 'http://www.cwi.nl/%7Eguido/Python.html?Name=Shubh%20Gohil&College=COEP'
query4 = 'Name=Shubh%20Gohil,Advait%20Gohil&College=COEP'

#a = urlparse(query)
#print(a)
#print(urllib.parse.parse_qs(query))
#print(urlparse(query1))
#print(urlparse(query2))
#print(urlparse(query3))
#print(urlparse(query4))

def resolve(element):
	params = urllib.parse.parse_qs(element)
	for key in params:
		string = params[key][0]
		params[key] = string
	return params

print(resolve(query4))

