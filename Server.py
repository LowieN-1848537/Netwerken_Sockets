import select
import socket
host = 'localhost'
port = 5000
#socket af_inet --> IPV4 standard
listening_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket_stream --> TCP
listening_Socket.bind((host, port))
listening_Socket.listen(1) # we specify that we only listen to 1 connection
listening_Socket.setblocking(True)
"""
conn, addr = listening_Socket.accept() # Wait for, and then accept, incoming client request
print ('Connected by %s' %str( addr))
while True:
    data = conn.recv(1024).decode('utf-8') # Wait for, and then receive, incoming data
    if not data:
        print("Connection closing")
        break #we break the while loop
    # Send some data back to the client
    print(data)
    conn.sendall(data.encode('utf-8')) #we send back the data so it just echo's what we received
conn.close()
listening_Socket.close()
"""

list_sockets = [ listening_Socket ]
nicknames = {}
def sendToAllSockets( data):
    print("sending message to connected sockets")
    for sock in list_sockets:

        if sock != listening_Socket: #this means this is a connected socket
            print(sock.getpeername()[1])
            print(nicknames[sock.getpeername()[1]])
            sock.sendall(data.encode('utf-8'))

while True:
    readable, writeable, exceptional = select.select(
    list_sockets, [], list_sockets
    )
    for sock in readable:
        if sock == listening_Socket:
            # TODO: Handle incoming client connection request
            conn, addr =sock.accept()
            print('new connection by %s' % str(addr))
            list_sockets.append(conn) # we add it to our list of connected sockets
        else:
            data = sock.recv(1024).decode('utf-8')  # Wait for, and then receive, incoming data
            if not data:
                print("Connection closing")
                list_sockets.remove(sock)
                sock.close()
            # Send some data back to the client
            else:
                if data.startswith('NICKNAME:'):
                    data.removeprefix('NICKNAME:')
                    socketPeer = sock.getpeername()[1]
                    print("nickname set:" + data)
                    nicknames[socketPeer] =data
                else:
                    print(data)
                    sendToAllSockets(data)
                    #sock.sendall(data.encode('utf-8'))
