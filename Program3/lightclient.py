# client.py
# Name: Jackson Hidley

import socket
import sys 
import getopt 
import argparse
import struct
import binascii

def create_packet(**info):
    print(info)
    version = socket.htons(info['message_version'])
    type = socket.htons(info['message_type'])
    length = info['message_string']
    data = struct.pack('!I', version) #pack the version
    data += struct.pack('!I', type) #pack the type
    data += struct.pack("!I", len(length)) #pack the length of string
    data += length.encode() #pack the data
    return data

def main():
    version = 17
    message = "Hello"
    hello_packet = create_packet(message_version=version, message_type = 1, message_string=message)

    message = "LIGHTON"
    command_on = create_packet(message_version=version, message_type = 2, message_string=message)

    message = "LIGHTOFF"
    command_off = create_packet(message_version=version, message_type = 2, message_string=message)


    #read command line arguments, IP and port
    ##sanity check inputs
    try:
        parser = argparse.ArgumentParser(description="CLIENT")
        parser.add_argument('-s', type=str, required=True, help='Server IP')
        parser.add_argument('-p', type=int, required=True, help='Port')
        parser.add_argument('-l', type=str, required=True, help='logFile')
        args = parser.parse_args()
        ip = args.s
        port = args.p
        log_file = args.l
    except:
        file = open(log_file + ".txt", "a")
        file.write("Error with command line arguments" + "\n")
        file.close()
        print("Error with command line arguments" + "\n")
    #Create a socket object, use TCP socket(SOCK_STREAM) for this assignment
    ##Check for errors
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err: 
         print ("socket creation failed with error %s" %(err) + "\n")
         file = open(log_file + ".txt", "a")
         file.write("socket creation failed with error %s" %(err) + "\n")
         file.close()
    #Connect to the IP and port read from command line
    ##handle connection failure
    try:
        s.connect((ip, port))
        print("Connected to server" + "\n")
    except:
        print("Error connecting")
        file = open(log_file + ".txt", "a")
        file.write("Error connecting" + "\n")
        file.close()


#send Hello packet to server
    s.sendall(hello_packet) # send message
    print("Sending HELLO")
    file = open(log_file + ".txt", "a")
    file.write("Sending HELLO Packet" + "\n")
    file.close()
#receive message from the server
    while(True): 
        #receive servers reply
        data = s.recv(struct.calcsize('!III'))
        version_raw, message_type_raw, length_raw = struct.unpack('!III',data)
        version = socket.ntohs(version_raw)
        message_type = socket.ntohs(message_type_raw)
        length = socket.ntohs(length_raw)

        print ('Received Data: version: {0:d} type: {1:d} length: {2:d}'.format(version, message_type, length))

        #check for version match
        if version == 17:
            print("VERSION ACCEPTED")
            file = open(log_file + ".txt", "a")
            file.write("VERSION ACCEPTED" + "\n")
            file.close()
        else:
            print("VERSION MISMATCH")
            file = open(log_file + ".txt", "a")
            file.write("VERSION MISMATCH" + "\n")
            file.close()
        #receive hello message from server
        message = s.recv(length).decode()
        print("Received Message: ", message)
        file = open(log_file + ".txt", "a")
        file.write("Received Message: " + message + "\n")
        file.close()
        #send COMMAND message to server
        if message_type == 1:
            print("Sending command")
            file = open(log_file + ".txt", "a")
            file.write("Sending command" + "\n")
            file.close()
            s.sendall(command_on) #or send off by using "command_off"
            print("SUCCESS")
            file = open(log_file + ".txt", "a")
            file.write("SUCCESS" + "\n")
            file.close()
        #send DISCONNECT message to server
        elif message_type == 2 and message == "SUCCESS":
                print("Command Successful")
                file = open(log_file + ".txt", "a")
                file.write("Command Successful" + "\n")
                file.close()
                break

    #close connection and file
    print("Closing Socket")
    file = open(log_file + ".txt", "a")
    file.write("Closing socket" + "\n")
    file.close()
    s.close()




main()