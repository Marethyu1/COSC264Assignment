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

if __name__ == '__main__':
    #makes it run automatically which is neat
    main()
