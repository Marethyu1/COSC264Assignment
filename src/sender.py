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
   # sock.send(b'Hello Liz and Stefan!')  # Remember, bytes not strings
    next = 0
    exitFlag = False

    #NOW ENTER LOOP

    """Attempt to read up to 512 byes from file to buffer. n = number of bytes actually read
        If n==0 prepare packet:
            *magicno = 0x497E
            *type = dataPacket
            *seqno = next
            *datalen = 0
            and empty data field
            Set exitFlag = True
        Else (n > 0)
            *magicno = 0x497E
            *type = acknowledgementPacket
            *seqno = rcvd.seqno
            *datalen = n
            Append n bytes of data to it
        Place packet into packetBuffer
        ENTERING INNER LOOP
            Send packet in packetBuffer via SOUT
            Wait for response on SIN (for AT MOST 1 SECOND) ...can use select()
            If no response
                go back to start of inner loop
            If response received
                if(rcvd.magicno != 0x497E || rcvd.type != acknowledgementPacket || rcvd.dataLen != 0)
                    go back to start of inner loop & retransmit packetBuffer
                else if rcvd.seqno != next
                    go back to start of inner loop & retransmit packetBuffer
                else rcvd.seqno == next
                    toggle next
                    if exitFlag == true
                        close file & exit sender
                    else (exitflag ==false)
                        go back to beginning of outer loop (read next block of data & try to transmit)

        Also add code that allows the sender to count how many packets it has sent in total over SOUT.
        Print this when program exits
                    """






if __name__ == '__main__':
    #makes it run automatically which is neat
    main()




































