import argparse
import socket
import sys 
import getopt 
from random import randint

try:
    parser = argparse.ArgumentParser(description="SERVER")
    parser.add_argument('-p', type=int, required=True, help='Port')
    parser.add_argument('-l', type=str, required=True, help='logFile')
    args = parser.parse_args()
    server_port = args.p
    log_file = args.l
    HOST = '192.168.56.1'
except:
    print("Errorr in getting the arguments")

#Step 2: #Create a socket object, use TCP socket(SOCK_STREAM) for this assignment
##Check for errors
file = open(log_file + ".txt", "w")
try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

except socket.error as err: 
        print ("Socket creation failed with error %s" %(err))
        file.write("Socket creation failed with error %s" %(err))
file.close()

#Step 3: #bind and listen
##handle bind failure
file = open(log_file + ".txt", "a")
try:
    s.bind((HOST, server_port))
    print("Bind Succeeded")
    file.write("Bind Succeeded\n")
except socket.error as errMessage:
    print("Bind Failed. Error code: %s" %(errMessage))
    file.write("Bind Failed. Error code: %s" %(errMessage) + "\n")
file.close() 

while(True):
    s.listen(9)


    #Step 4: #receive a message from the client, check for the work “network”
    conn, addr = s.accept()
    print("Received connection from " + str(addr) + ", " + str(conn) + "\n")
    file = open(log_file + ".txt", "a")
    file.write("Connection from: " + str(addr) + ", " + str(conn) + "\n")
    file.close()

    message = str(conn.recv(1024))

    file = open(log_file + ".txt", "a")
    file.write("Recieved message: " + message + "\n")
    file.close()
    print("Recieved message: " + message)

    if "Network" in message or "network" in message or "NETWORK" in message:
        print("Network is in message.")
        file = open(log_file + ".txt", "a")
        file.write("Network is in message." + "\n")
        file.close()

    #Step 5: pick a random quote and send to the client
    rand = int(randint(0,29))

    with open("quotes.txt") as fileIn:
        line = ""
        for i in range(rand):
            line = fileIn.readline()
    fileIn.close()

    conn.send(line.encode()) 

    #Step 6: Make sure to log all interactions
    file = open(log_file + ".txt", "a")
    file.write("Sending quote: " + line)
    file.close()
    

s.close()
