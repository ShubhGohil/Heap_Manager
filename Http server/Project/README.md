HTTP SERVER

This is a project on Http Server made by Shubh Gohil.

It can handle:
GET, POST, PUT, HEAD, DELETE, Cookies, Headers, non-persistent connections, Multiple clients at the same time (with a sepearate program to test this), handling file permissions;  Server configuration - config file with DocumentRoot, log file name, max simulateneous connections ;


On the way of how to run the server, this directory contains 2 files
1.server.py
You can run on your terminal, using $ python3 server.py

To test this program you can use a browser like Firefox or Chrome or can be used by making a client script can running it.
The scrpits are given in stresstest1.py and stresstest2.py
You will have to run this scripts $ python3 stresstest{num}.py
(The server should already be while performing this tests)

To know more about configuration of the system visit exite.conf file.

References:
1. https://tools.ietf.org/html/rfc2616
2. https://github.com/sm8799/HTTP-Web-Server/blob/master/webserver.py
3. https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/
