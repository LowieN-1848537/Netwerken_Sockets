import select
import sys
import threading
import socket


#list of msg's to be sent
mutex = threading.Lock()
HOST = "localhost"  # The server's hostname or IP address
PORT = 5000  # The port used by the server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))  # we connect to the server using tcp


def thread_Connection():
    print("thread_Connection runnning")
    global sock
    global mutex
    list_sockets = [sock]
    #this is our connection thread

    sock.sendall("JOIN: listener".encode("utf-8"))
    while True:
        # Check whether user provided input via console

        readable, writeable, exceptional = select.select(
            list_sockets, [], list_sockets, 1
        )
        for s in readable:
            data = s.recv(1024).decode('utf-8')  # Wait for, and then receive, incoming data
            if data:
                print(data)



if __name__ == '__main__':
    thread_list = []
    # Start a thread to read user input
    #start a thread for receiving messages
    receiveThread = threading.Thread(target=thread_Connection,daemon=True)

    receiveThread.start()
    thread_list.append(receiveThread)
    for thread in thread_list:
        thread.join()
     #thread_read_user_input()
    #t.run()
    #receiveThread.run()