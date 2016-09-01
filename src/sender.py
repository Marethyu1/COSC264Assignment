"""
Sender part of assignment
#--Liz And Stefan--#
To run me type in the command line:
python sender.py portNum PortNum PortNum fileName
"""

import sys
import socket
import os.path #This is being used to check if file exists
import struct
import binascii
import packets
import select

MAX_BYTES = 512


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


def read_file_data(file_obj):
    return file_obj.read(MAX_BYTES)








def main():
    #this is the main function which does the business
    SIN, SOUT, CSIN, FILENAME = get_params()
    #print(SIN, SOUT, CSIN, FILENAME)

    sockOut = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sockOut.bind(('127.0.0.1', SOUT))
    sockOut.connect(('127.0.0.1', CSIN))  # So we don't have to specify where we send to
    sockOut.setblocking(0)

    sockIn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sockIn.bind(('127.0.0.1', SIN))
    sockIn.setblocking(0)
    # sock.send(b'Hello Liz and Stefan!')  # Remember, bytes not strings
    next = 0
    exitFlag = False

    #NOW ENTER LOOP

    file_object = open(FILENAME, "rb")

    #current_string = read_file_data(file_object)
    """print(file_string)
    print()

    while len(file_string) != 0:
        file_string = read_file_data(file_object)
        print(file_string)
        print()
    """
    count  = 0
    while not exitFlag:
        current_string = read_file_data(file_object)
        if len(current_string) == 0:
            current_packet = packets.packet(next, len(current_string), current_string)
            exitFlag = True
            print("HUASDASD")
            #print(current_packet)

        elif len(current_string) > 0:
            current_packet = packets.packet(next, len(current_string), current_string)
            #print(current_packet)


        encoded_packet = packets.pack_packet(current_packet)

        has_response = False
        while not has_response:
            sock.send(encoded_packet) #sendencoded packet

            readable, _, _ = select.select([sock], [], [], 1)
            if readable:
                data = sock.recv(528)
                has_response = True
                print(data)

        next ^= 1 #XOR Using bitwise operator

    print("weeees")
    file_object.close()



    """ENTERING INNER LOOP
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

    """
       while True:

           message = input()
           message = str.encode(message, 'utf-8')
           sock.send(message)  # Remember, bytes not strings

           # data, sender = sock.recvfrom(SOUT)
           # data = data.decode('utf-8')
           # if data:
           #     print("recieved: ", data)

       """




if __name__ == '__main__':
    #makes it run automatically which is neat
    main()




































