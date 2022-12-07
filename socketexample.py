import socket
import sys 
import getopt 

def client_program():
    host = None
    port = None
    logfile = None
    argv = sys.argv[1:] 
    
    try: 
        opts, args = getopt.getopt(argv, "f:l:") 
        
    except: 
        print("Error") 
    
    for opt, arg in opts: 
        if opt in ['-s']: 
            ip = arg 
        elif opt in ['-p']: 
            port = arg 
        elif opt in ['-l']:
            logfile = arg

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:  # instantiate
        client_socket.connect((host, port))  # connect to the server

        message = input(" -> ")  # take input

        while message.lower().strip() != 'bye':
            client_socket.send(message.encode())  # send message
            data = client_socket.recv(1024).decode()  # receive response

            print('Received from server: ' + data)  # show in terminal

            message = input(" -> ")  # again take input

        client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
        data = input(' -> ')
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


#if __name__ == '__main__':
#    server_program()