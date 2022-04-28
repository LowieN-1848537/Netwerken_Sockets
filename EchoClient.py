import socket

HOST = "localhost"  # The server's hostname or IP address
PORT = 5000  # The port used by the server
s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT)) #we connect to the server using tcp
s.sendall("Hello world of s1!".encode('utf-8'))
data = s.recv(1024).decode('utf-8')
print(f"Received {data!r}")
# s.close()

s2 =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.connect((HOST, PORT))  # we connect to the server using tcp
s2.sendall("Hello world of s2!".encode('utf-8'))
data2 = s2.recv(1024).decode('utf-8')
print(f"Received {data2!r}")

s.sendall("Hello world of s1!".encode('utf-8'))
data = s.recv(1024).decode('utf-8')
print(f"Received {data!r}")
s.close()
s2.sendall("Hello world of s2!".encode('utf-8'))
data2 = s2.recv(1024).decode('utf-8')
print(f"Received {data2!r}")
s2.close()