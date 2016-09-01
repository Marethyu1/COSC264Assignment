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
        SIN = checkPort(sys.argv[0])
        SOUT = checkPort(sys.argv[1])
        CSIN = checkPort(sys.argv[2]) #NOTE: Not sure if this needs to be in the same range?
        FILENAME = checkFile(sys.argv[3])

    return  SIN, SOUT, CSIN, FILENAME


def read_file_data(file_obj):
    return file_obj.read(MAX_BYTES)


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
    SIN, SOUT, CSIN, FILENAME = get_params()
    #print(SIN, SOUT, CSIN, FILENAME)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', SIN))
    sock.connect(('127.0.0.1', SOUT))  # So we don't have to specify where we send to
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
            current_packet = packet(next, len(current_string), current_string)
            #print(current_packet)

        elif len(current_string) > 0:
            current_packet = packet(next, len(current_string), current_string)
            #print(current_packet)


        encoded_packet = pack_packet(current_packet)
        sock.send(encoded_packet)

        #print(encoded_packet)
       #unpacked_packet = unpack_packet(encoded_packet)


        count += 1

        if count == 10:
            exitFlag = True


    file_object.close()
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




































