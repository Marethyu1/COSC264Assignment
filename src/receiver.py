"""
Receiver part of assignment
#--Liz And Stefan--#
To run me type in the command line:
python3 receiver.py portNum PortNum PortNum fileName
"""

import sys
import socket
import os.path #This is being used to check if file exists


def exit():
    #exits program
    print("Program will now exit\n")
    sys.exit(0)

def checkPort(num):
    #checks to make sure the entered port number is an int
    try:
        port_num = int(num)
    except ValueError:
        print("Port Number " + str(num) + " was not an integer")
        exit()
        
    if not(1024 <= port_num and port_num <= 64000):
        #checking range
        print("Port number " + str(num) + "  was not in range 1024 - 64000")
        exit()
        
    else:
        return port_num
    
def checkFile(fname):
    """checks for existing file"""
    if(os.path.isfile(fname)):
        return fname
    else:
        print("File: " + fname + " does not exist.")
        exit()
    

def get_params():
    #gets and sets all of the inputs from the command line
    #print(sys.argv)
    if len(sys.argv) != 5:
        #error Checking
        print("\nWrong amount of command line arguments entered")
        
        exit()
        
    else:    
        sys.argv = sys.argv[1:] #chops of name of program
        RIN = checkPort(sys.argv[0])
        ROUT = checkPort(sys.argv[1])
        CRIN = checkPort(sys.argv[2]) #NOTE: Not sure if this needs to be in the same range?
        FILENAME = checkFile(sys.argv[3])
        
        
        
        
    return  RIN, ROUT, CRIN, FILENAME
    

def main():
    #this is the main function which does the business
    RIN, ROUT, CRIN, FILENAME = get_params()
    print(RIN, ROUT, CRIN, FILENAME)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # sets IP, UDP
    sock.bind(('127.0.0.1', RIN))  # Claim the port for the server to use
    sock.connect(('127.0.0.1', ROUT))

    while True:

        print("I AM LISTENING")


        data, sender = sock.recvfrom(ROUT) #chang to CRIN when we have a channel set up
        data = data.decode('utf-8')
        print("recieved: ", data)


        if data == "hello":
            message = input()
            message = str.encode(message, 'utf-8')
            sock.send(message)  # Remember, bytes not strings






        # data, sender = sock.recvfrom(1024)  # Get some data, blocking
        # if data == b'request-time':  # b is for bytes, strings are too fancy
        #     now = datetime.datetime.now().strftime("%I:%M:%S%p on %B %d, %Y")
        #     sock.sendto(bytes(now, 'utf8'), sender)  # Reply back to sender with bytes
        # else:
        #     print("BAD PACKET")




if __name__ == '__main__':
    #makes it run automatically which is neat
    main()






























