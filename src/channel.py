"""
Channel part of assignment
#--Liz And Stefan--#

To run me type in the command line:
python channel.py portNum PortNum PortNum PortNum S(in) R(in) P
"""

import sys
import socket



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
    

def checkProbability(p):
    try:
        p = float(p)
    except ValueError:
        print("Probability not an integer")
        exit()
    else:
        
        if not(0 <= p < 1):
            print("Probability not in range 0-1")
            exit()
        else:
            return p

def get_params():
    #gets and sets all of the inputs from the command line
    #print(sys.argv)
    if len(sys.argv) != 8:
        #error Checking
        print("\nWrong amount of command line arguments entered")
        
        exit()
        
    else:    
        sys.argv = sys.argv[1:] #chops of name of program
        CSIN = checkPort(sys.argv[0])
        CSOUT = checkPort(sys.argv[1])
        CRIN = checkPort(sys.argv[2])
        CROUT = checkPort(sys.argv[3])
        
        SIN = checkPort(sys.argv[4]) #NOTE NOT SURE IF WE NEED TO CHECK PORT OR IF WE CAN JUST TURN INTO INT
        RIN = checkPort(sys.argv[5])
        
        P = checkProbability(sys.argv[6])

        
    return  CSIN, CSOUT, CRIN, CROUT, SIN, RIN, P
    

def main():
    #this is the main function which does the business
    CSIN, CSOUT, CRIN, CROUT, SIN, RIN, P = get_params()

    sockCSOut = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sockCSOut.bind(('127.0.0.1', CSOUT))
    sockCSOut.connect(('127.0.0.1', SIN))  # So we don't have to specify where we send to
    sockCSOut.setblocking(0)

    sockCSIn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sockCSIn.bind(('127.0.0.1', CSIN))
    sockCSIn.setblocking(0)

    sockCROut = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sockCROut.bind(('127.0.0.1', CROUT))
    sockCROut.connect(('127.0.0.1', RIN))  # So we don't have to specify where we send to
    sockCROut.setblocking(0)

    sockCRIn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sockCRIn.bind(('127.0.0.1', CRIN))
    sockCRIn.setblocking(0)

    senderSocket =   socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    recieverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)






if __name__ == '__main__':
    #makes it run automatically which is neat
    main()