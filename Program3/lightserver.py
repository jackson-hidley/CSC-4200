import argparse
import socket
import sys 
import getopt 
from random import randint
import struct
import binascii



def create_packet(**info):
    print(info)
    v = socket.htons(info['message_version'])
    t = socket.htons(info['message_type'])
    s = info['message_string']
    data = struct.pack('!I', v) #pack the version
    data += struct.pack('!I', t) #pack the version
    data += struct.pack("!I", len(s)) #pack the length of string
    data += s.encode() #pack the data
    return data

#for the command lightOn and lightOff
#currently does nothing
def run_command(command):
    return 0

#get arguments from command line
try:
    parser = argparse.ArgumentParser(description="CLIENT")
    parser.add_argument('-p', type=int, required=True, help='Port')
    parser.add_argument('-l', type=str, required=True, help='logFile')
    args = parser.parse_args()
    port = args.p
    log_file = args.l
except:
    print("Error with command line arguments")
#create hello packet
version =17
hello_message = "Hello"
hello_packet = create_packet(message_version=version, message_type = 1,message_string=hello_message)

#create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((socket.gethostname(), port))
sock.listen(5) #backlog
file = open(log_file + ".txt", "w")
file.write("Binded"+ "\n")
file.close()
while True:
    connection, address = sock.accept()
    print("Received connection from (IP, PORT): ", address)
    file = open(log_file + ".txt", "a")
    file.write("Received connection from (IP, PORT): " + str(address) + "\n")
    file.close()
    
    try:
        while True:
            data = connection.recv(struct.calcsize('!III'))

            if len(data) == 0:
                break

            #version, message_type, length = struct.unpack('!III',data)
            version_raw, message_type_raw, length_raw = struct.unpack('!III',data)
            version = socket.ntohs(version_raw)
            message_type = socket.ntohs(message_type_raw)
            length = socket.ntohs(length_raw)
            print ('Received Data: version: {0:d} message_type: {1:d} length: {2:d}'.format(version, message_type, length))
            file = open(log_file + ".txt", "a")
            file.write('Received Data: version: {0:d} message_type: {1:d} length: {2:d}'.format(version, message_type, length) + "\n")
            file.close()
            if version == 17: #correct version
                print("VERSION ACCEPTED")
                file = open(log_file + ".txt", "a")
                file.write("VERSION ACCEPTED"+ "\n")
                file.close()
                message = connection.recv(length).decode()
            else:
                print("VERSION MISMATCH")
                file = open(log_file + ".txt", "a")
                file.write("VERSION MISMATCH")
                file.close()
            if message_type == 1: #hello packet
                connection.sendall(hello_packet)
            elif message_type == 2: #command packet: LIGHTON
                print("EXECUTING SUPPORTED COMMAND: ", message+ "\n")
                file = open(log_file + ".txt", "a")
                file.write("EXECUTING SUPPORTED COMMAND: " + message + "\n")
                file.close()
                com = run_command(message)
                if com == 0: #success
                    connection.sendall(create_packet(message_version=version, message_type = 2,message_string="SUCCESS"))

            else:
                print("IGNORING UNKNOWN COMMAND: ", message)
                file = open(log_file + ".txt", "a")
                file.write("IGNORING UNKNOWN COMMAND: ", message + "\n")
                file.close()
                

    finally:
        file = open(log_file + ".txt", "a")
        file.write("DISCONNECTED" + "\n")
        file.close()
        connection.close()