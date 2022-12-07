import socket
import threading
#
#HOST = '34.125.218.135'
#PORT = 8001
#
#class Client:
#    def __init__(self, host, port):
#        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        self.sock.connect((host, port))
#        
#        receive_thread = threading.Thread(target=self.receive)
#        receive_thread.start()
#
#    def write(self, message):
#        message = message.encode('utf-8')
#        self.sock.send(message)
#
#    def stop(self):
#        self.sock.close()
#
#    def receive(self):
#        while True:
#            try:
#                message = self.sock.recv(1024).decode('utf-8')
#                print(message)
#            except ConnectionAbortedError:
#                break
#            except:
#                print("Error")
#                self.socket.close()
#
#client = Client(HOST, PORT)

def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


client_program()