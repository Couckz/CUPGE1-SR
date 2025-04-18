import socket
IP = "127.0.0.1"
PORT = 8080
MESSAGE = "GET /pages/index.html HTTP/1.1\r\nHost: localhost\r\nAccept-Language: fr\r\n\r\n".encode("utf-8")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((IP, PORT))
s.send(MESSAGE)
data = s.recv(1024)
print(data)
s.close()

