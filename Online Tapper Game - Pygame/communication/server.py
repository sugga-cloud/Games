import socket

server = socket()
host = ""
port = 8080

server.bind((host,port))

server.listen(2)
running = True

user = {}

while running:
    client,address = server.accept()
    