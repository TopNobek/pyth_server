import socket
import sys
import os

HOST = ''                 # Symbolic name meaning the local host
PORT = 8080              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print ('Connected by', addr)

def parse_request(data):
    data = data.decode('utf-8')
    data = data.splitlines()
    verb, path, ver = data[0].split(" ")
    
    if ".." in path or not path.startswith("/"):
        raise Exeption("cya")

    if path == "/":
        path = "/index.html"

    path = "html" + path
    return verb, path, ver;

def check_content(path):
    ext = path.split(".")
    ext = ext[1]

    if ext == 'html':
        return 'text/html'
    elif ext == 'ico':
        return 'image/x-icon'
    elif ext == 'png':
        return 'image/png'
    else:
        return 'application/binary'

def response(path):
    if os.path.exists(path) == False:
        code = 404;
        f = ''
    else:
        code = 200;
        f = open(path, "rb")
        f = f.read()

    conn.sendall(("HTTP/1.1 %i OK\r\n" % code).encode())
    conn.sendall(("Content-Length: %i\r\n" % len(f)).encode())
    conn.sendall(("Content-Type: %s\r\n" % check_content(path)).encode())
    conn.sendall(("\r\n").encode())
    conn.sendall(f)

while 1:
    data = conn.recv(1024)
    print (data)
    verb, path, ver = parse_request(data)
    print (verb)
    print (path)
    print (ver)
    
    response(path)
    if not data: break

conn.close()
