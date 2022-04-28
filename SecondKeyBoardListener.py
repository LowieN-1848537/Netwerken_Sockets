import select
import sys
import threading
import socket


#list of msg's to be sent
list_pending_messages = [] # data structure to store unprocessed user input mutex = threading.Lock() # to coordinate multi-threaded access to shared memory (= list_pending_messages)
mutex = threading.Lock()
HOST = "localhost"  # The server's hostname or IP address
PORT = 5000  # The port used by the server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))  # we connect to the server using tcp


def thread_Connection():
    print("thread_Connection runnning")
    global sock
    global list_pending_messages
    global mutex
    list_sockets = [sock]
    #this is our connection thread
    while True:
        # Check whether user provided input via console
        mutex.acquire()
        for str_msg in list_pending_messages:

            sock.sendall(str_msg.encode('utf-8'))
        list_pending_messages = [] #we clear the list after all were sent
        mutex.release()
        readable, writeable, exceptional = select.select(
            list_sockets, [], list_sockets, 1
        )
        for s in readable:
            data = sock.recv(1024).decode('utf-8')  # Wait for, and then receive, incoming data
            if data:
                print("We received a message:")
                print(data)


def thread_read_user_input():
    global list_pending_messages
    global mutex
    print("thread_read_user_input running")
    while True:
        str_msg = sys.stdin.readline()
        str_msg = str_msg.rstrip('\r\n') # drop trailing newline (added automatically by stdin.readline)
        mutex.acquire()
        list_pending_messages.append(str_msg)
        mutex.release()


if __name__ == '__main__':
    thread_list = []
    # Start a thread to read user input
    inputreadThread = threading.Thread(target=thread_read_user_input, daemon=True)


    #start a thread for receiving messages
    receiveThread = threading.Thread(target=thread_Connection,daemon=True)
    inputreadThread.start()

    receiveThread.start()


    thread_list.append(inputreadThread)
    thread_list.append(receiveThread)
    for thread in thread_list:
        thread.join()
     #thread_read_user_input()
    #t.run()
    #receiveThread.run()