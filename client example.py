# client.py
# Name: Jackson Hidley

import socket
import sys 
import getopt 
    



def main():
    
    #read command line arguments, IP and port
    ##sanity check inputs
    ip = '34.125.218.135'
    port = 8001
    logfile = "LOGFILE"
    argv = sys.argv[1:] 
    
    #try: 
    #    opts, args = getopt.getopt(argv, "f:l:", ["ip=", "port=", "logfile="]) 
#
    #    for opt, arg in opts: 
    #        if opt in ['-s']: 
    #            ip = arg 
    #        elif opt in ['-p']: 
    #            port = arg 
    #        elif opt in ['-l']:
    #            logfile = arg
    #except:  
    #    print("Error") 

    #Create a socket object, use TCP socket(SOCK_STREAM) for this assignment
    ##Check for errors
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        #s.bind((ip, port))
        s.listen()
        #conn, addr = s.accept()
        #with conn:
        #    print(f"Connected by {addr}")
        while True:
            #Connect to the IP and port read from command line
            data = s.recv(1024).decode()
            #data = conn.recv(1024)
            ##handle connection failure
            if not data:
                break
            s.send(data)

    except socket.error as err: 
         print ("socket creation failed with error %s" %(err))



#read a message from user
    message = input(" -> ")
#Send message to the server
    s.send(message.encode())  # send message
#receive message from the server
    message = s.recv(1024).decode()
    print(message)
#Easter egg: You need to send a specific word “Network” to receive a Message.
    if "Network" in message:
        #print message
        print(message)
    print("end")

    #close connection
    s.close()




main()