"""
Sender part of assignment
#--Liz And Stefan--#
To run me type in the command line:
python sender.py portNum PortNum PortNum fileName
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
        SIN = checkPort(sys.argv[0])
        SOUT = checkPort(sys.argv[1])
        CSIN = checkPort(sys.argv[2]) #NOTE: Not sure if this needs to be in the same range?
        FILENAME = checkFile(sys.argv[3])
        
        
        
        
    return  SIN, SOUT, CSIN, FILENAME
    

def main():
    #this is the main function which does the business
    SIN, SOUT, CSIN, FILENAME = get_params()
    print(SIN, SOUT, CSIN, FILENAME)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', SIN))
    sock.connect(('127.0.0.1', SOUT))  # So we don't have to specify where we send to






    while True:

        message = input()
        message = str.encode(message, 'utf-8')
        sock.send(message)  # Remember, bytes not strings

        # data, sender = sock.recvfrom(SOUT)
        # data = data.decode('utf-8')
        # if data:
        #     print("recieved: ", data)





if __name__ == '__main__':
    #makes it run automatically which is neat
    main()




































