"""
Receiver part of assignment
#--Liz And Stefan--#
To run me type in the command line:
python3 receiver.py portNum PortNum PortNum fileName
"""

import sys
import socket
import os.path #This is being used to check if file exists
import struct
import binascii
import packets
import select


MAX_BYTES = 512
MAGICNO = hex(0x497E)
PTYPE_DATA = 0
PTYPE_ACK = 1

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
    sock.connect(('127.0.0.1', ROUT))  # So we don't have to specify where we send to
    sock.setblocking(0)

    expected = 0
    currentSeqno = 0

    poos_count = 0
    recieving_packets = True

    fileStream = bytearray()

    while recieving_packets:
        readable, _, _ = select.select([sock], [], [], 1)

        if readable:
            data, sender = sock.recvfrom(528)
            #print(data)
            unpacked_packet = packets.unpack_packet(data)
            magicno, type, seqno, dataLen, data = unpacked_packet
            #print(unpacked_packet)
            #
            if poos_count < 3:
                 type = 10000
                 poos_count += 1
                 print("hasnt recieved")
            if magicno == int(MAGICNO, 0) and type == PTYPE_DATA and seqno == expected: #add seqnoCheck

                ack_pack = packets.packet(currentSeqno)
                packed_packet = packets.pack_packet(ack_pack)

                print(data)
                #fileStream.append(bytearray(data), 256)

                sock.send(packed_packet)

                if dataLen == 0:
                    recieving_packets = False






        expected ^= 1


    print(fileStream)




    #ENTER LOOP

    """Wait on socket RIN for incoming packet. USE BLOCKING SYSTEM CALL
     if rcvd.magicno != 0x497E then STOP PROCESSING (go back to start of loop)
     if rcvd.type != expected STOP PROCESSING
     if rcvd.seqno != expected
        Prepare acknowledgement packet
            *magicno = 0x497E
            *type = acknowledgementPacket
            *seqno = rcvd.seqno
            *datalen = 0
        Send via ROUT to channel
        Stop processing
    If rcvd.seqno = expected:
        Prepare acknowledgement packet
            *magicno = 0x497E
            *type = acknowledgementPacket
            *seqno = rcvd.seqno
            *datalen = 0
            and empty data field
        Send via ROUT
        Toggle value of expected (swap from 0->1 or 1->0)
        If rcvd.dataLen > 0
            append data to output, stop processing
        Else (data contains to data.. rcvd.data:en == 0
            close output file and all sockets
            exit program"""



        # data, sender = sock.recvfrom(1024)  # Get some data, blocking
        # if data == b'request-time':  # b is for bytes, strings are too fancy
        #     now = datetime.datetime.now().strftime("%I:%M:%S%p on %B %d, %Y")
        #     sock.sendto(bytes(now, 'utf8'), sender)  # Reply back to sender with bytes
        # else:
        #     print("BAD PACKET")




if __name__ == '__main__':
    #makes it run automatically which is neat
    main()






























