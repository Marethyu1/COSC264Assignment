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

class packet:
    def __init__(self, seqno, dataLen, data, type=PTYPE_DATA, magicno=MAGICNO):
        self.magicno = magicno
        self.type = type
        self.seqno = seqno
        self.dataLen = dataLen
        self.data = data

    def isMagicno(self):
        """returns true if Magicno == """
        return self.magicno == MAGICNO

    def __str__(self):
        current_type = "dataPacket"
        if self.type == PTYPE_ACK:
            current_type = "acknowledgementPacket"
        out_string = "\ntype is {0}\nSeqno is {1}\nDataLen is {2}\nData is {3}\nmagicNo is {4}\n".format(current_type, self.seqno, self.dataLen, self.data, self.isMagicno())
        # a = ("Type is {0}\n".format(self.type))
        # b = ("Seqno is {0}\n".format(self.seqno))
        # c = ("DataLen is {0}\n".format(self.dataLen))
        # d = ("Data is {0}\n".format(self.data))
        # e = ("magicNo is {0}\n".format(self.magicno))
        return out_string

def pack_packet(current_packet):

    magicno = current_packet.magicno
    type = current_packet.type
    seqno = current_packet.seqno
    dataLen = current_packet.dataLen
    data = current_packet.data


    to_pack = (int(magicno, 0), type, seqno, dataLen, data)

    pack_format = 'I I I I {0}s'.format(dataLen)
    my_struct = struct.Struct(pack_format)
    packed_packet = my_struct.pack(*to_pack)

    return packed_packet

def unpack_packet(packed_packet):

    pack_format = 'I I I I {0}s'.format(len(packed_packet)-16)
    my_struct = struct.Struct(pack_format)
    #print(len(packed_packet))
    unpacked_packet = my_struct.unpack(packed_packet)
    # magicno = unpacked_packet[0]
    # type = unpacked_packet[1]
    # seqno = unpacked_packet[2]
    #dataLen = unpacked_packet[3]
    # data = unpacked_packet[4]

    return unpacked_packet

    

def main():
    #this is the main function which does the business
    RIN, ROUT, CRIN, FILENAME = get_params()
    print(RIN, ROUT, CRIN, FILENAME)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # sets IP, UDP
    sock.bind(('127.0.0.1', RIN))  # Claim the port for the server to use

    expected = 0

    while True:
        data, sender = sock.recvfrom(1024)
        unpacked_packet = unpack_packet(data)

        print(unpacked_packet[4])


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






























