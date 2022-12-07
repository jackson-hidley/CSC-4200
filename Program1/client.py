# client.py
# Name: Jackson Hidley

import socket
import sys 
import getopt 
import argparse



def main():
    
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
        print("Error with command line arguments" + "\n")
    file = open(log_file + ".txt", "w")

    #Create a socket object, use TCP socket(SOCK_STREAM) for this assignment
    ##Check for errors
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err: 
         print ("socket creation failed with error %s" %(err))

    #Connect to the IP and port read from command line
    ##handle connection failure
    try:
        s.connect((ip, port))
    except:
        print("Error connecting")
#read a message from user
    message = input(" -> ")
#Send message to the server
    s.send(message.encode())  # send message
#receive message from the server
    message = s.recv(1024).decode()
    print(message)
    file.write(message)
#Easter egg: You need to send a specific word “Network” to receive a Message.
    if "Network" in message:
        #print message
        print(message)
        file.write(message)

    #close connection and file
    s.close()
    file.close()




main()