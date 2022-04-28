import select
import socket
import threading

#these are important later on



def IRCChanges(data,listing,connection, prefix):
    data = data.removeprefix(prefix)
    socketPeer = connection.getpeername()[1]
    newdata = prefix + data
    print(newdata)
    listing[socketPeer] = data
    connection.sendall(newdata.encode('utf-8'))

def LeaveChannel(connection):
    global Channels
    try:
        Channels.pop(connection.getpeername()[1])
    except Exception as e:
        pass

def sendToAllSockets( data, connection):
    global nicknames
    global list_sockets
    global Channels
    exData =""
    channel = ""
    #here we set the name in front if the user has a nickname
    try:

        data = nicknames[connection.getpeername()[1]] + " said: " + data
    except Exception as e:
        pass
    try:

        channel = Channels[connection.getpeername()[1]]
    except Exception as e:
        pass

    for sock in list_sockets:
        exData = data
        if sock != listening_Socket: #this means this is a connected socket
            socketChannel = ""
            try:
                socketChannel = Channels[sock.getpeername()[1]]

            except Exception as e:
                pass
            if channel == "":
                sock.sendall(exData.encode('utf-8'))
            elif channel == socketChannel:
                exData += " in channel: " + channel
                sock.sendall(exData.encode('utf-8'))


def removeFromsessions(sock):
    global nicknames
    global Channels
    try:
        nicknames.pop(sock.getpeername()[1] )
    except Exception as e:
        pass
    try:
        Channels.pop(sock.getpeername()[1])
    except Exception as e:
        pass


#This thread handles all of the data that was received and put in the buffer
def Thread_BufferHandler():
    global ServerReadBuffer
    global mutex
    while True:
        mutex.acquire()
        if ServerReadBuffer != []:
            (msg,sock) = ServerReadBuffer[0]
            if msg.startswith('NICK: '):
                IRCChanges(msg, nicknames, sock, 'NICK: ')
            elif msg.startswith('JOIN: '):
                IRCChanges(msg, Channels, sock, 'JOIN: ')
            elif msg.startswith('LEAVE: '):
                LeaveChannel(sock)
            else:
                print(msg)
                sendToAllSockets(msg, sock)
            ServerReadBuffer.pop(0)
        mutex.release()


#this thread receives data from connected sockets and puts them in a buffer to be handled by worker threads
def Thread_Receiver():
    global mutex
    global ServerReadBuffer
    global list_sockets
    global listening_Socket
    while True:
        readable, writeable, exceptional = select.select(
            list_sockets, [], list_sockets
        )
        for sock in readable:
            if sock == listening_Socket:
                conn, addr = sock.accept()
                print('new connection by %s' % str(addr))
                list_sockets.append(conn)  # we add it to our list of connected sockets
            else:
                try:
                    data = sock.recv(1024).decode('utf-8')  # Wait for, and then receive, incoming data
                    if not data:
                        print("Connection closing")
                        list_sockets.remove(sock)
                        sock.close()
                    # Send some data back to the client
                    else:
                        mutex.acquire()
                        #here we set our buffer to 20000 if another piece of data comes in we just don't let it enter the buffer
                        if len( ServerReadBuffer) < 20000:
                            ServerReadBuffer.append((data,sock))

                        mutex.release()
                except Exception as e:
                    # in the event we lose connection with a socket we disconnect it on the serverside aswell
                    print("disconnecting user")
                    removeFromsessions(sock)
                    sock.close()
                    list_sockets.remove(sock)


if __name__ == '__main__':
    thread_list =[]

    host = 'localhost'
    port = 5000
    #socket af_inet --> IPV4 standard
    global listening_Socket
    listening_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket_stream --> TCP
    listening_Socket.bind((host, port))
    listening_Socket.listen(1) # we specify that we only listen to 1 connection
    listening_Socket.setblocking(True)
    global list_sockets
    list_sockets= [ listening_Socket ]
    global nicknames
    global Channels
    nicknames = {}
    Channels = {}
    #here we define a buffer that will save some of our data in the event that processing doesn't go fast enough.
    #idealy we set this on a seperate Thread
    global ServerReadBuffer
    ServerReadBuffer = []
    global mutex
    mutex = threading.Lock()

    inputThread = threading.Thread(target=Thread_Receiver,daemon=True)
    inputThread.start()
    bufferHandler = threading.Thread(target=Thread_BufferHandler(),daemon=True)
    bufferHandler.start()

    thread_list.append(inputThread)
    thread_list.append(bufferHandler)
    for thread in thread_list:
        thread.join()
