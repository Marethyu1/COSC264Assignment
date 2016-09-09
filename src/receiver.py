"""
Receiver part of assignment
#--Liz And Stefan--#
To run me type in the command line:
python3 receiver.py portNum PortNum PortNum fileName
# python3 receiver.py 9000 9001 8003 test.txt
"""



import sys
import socket
import os.path
import packets
import select


MAX_BYTES = 512
MAGICNO = hex(0x497E)
PTYPE_DATA = 0
PTYPE_ACK = 1

def exit():
    """Exits the program displaying a message"""
    print("----------------------------------------")
    print("------------Program exited--------------")
    print("----------------------------------------")
    sys.exit(0)

def checkPort(num):
    """checks port number to ensure that it is an integer in the range 1024 - 64000
        exits program if it finds and error
        returns portnumber as an integer"""
    try:
        port_num = int(num)
    except ValueError:
        print("Port Number " + str(num) + " was not an integer")
        exit()
    if not(1024 <= port_num and port_num <= 64000):
        print("Port number " + str(num) + "  was not in range 1024 - 64000")
        exit()
        
    else:
        return port_num
    
def checkFile(fname):
    """checks for existing file
        exits if file not found"""
    if(os.path.isfile(fname)):
        print("File: " + fname + " already exists.")
        exit()

    else:

        return fname
    

def get_params():
    """gets all of the parameters from the command line
        exits if wrong amount of arguments are entered
        checks to ensure input is correct
        returns port numbers and filename"""
    if len(sys.argv) != 5:
        print("\nWrong amount of command line arguments entered")
        exit()
    else:    
        sys.argv = sys.argv[1:]
        rin = checkPort(sys.argv[0])
        rout = checkPort(sys.argv[1])
        crin = checkPort(sys.argv[2])
        filename = checkFile(sys.argv[3])

        
        
        
    return rin, rout, crin, filename

def  return_resources(socket_list):
    """closes sockets and file
        giving memory back to system"""
    for sockets in socket_list:
        sockets.close()

def raise_socket_error(socket_list, ERRORCOUNT=0):
    """if connection to a socket is refused an error is raised
        will wait 10 times and then time out"""

    if ERRORCOUNT>10:
        print()
        print("----------------------------------------")
        print("-----------Connection refused-----------")
        print("----------Program will now exit---------")
        print("----------------------------------------")
        print()

        return_resources(socket_list)
        exit()

    else:
        print()
        print("---connection refused, trying again-----")
        print()

    return ERRORCOUNT+1


def main():
    """Main function for reciever
     recieves data and turns into file
     sends ack packets"""
    rin, rout, CRIN, FILENAME = get_params()

    sockOut = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockOut.bind(('127.0.0.1', rout))
    sockOut.connect(('127.0.0.1', CRIN))

    sockIn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockIn.bind(('127.0.0.1', rin))

    expected = 0
    recieving_packets = True
    socket_list = [sockOut, sockIn]
    error_count = 0

    file_object = open(FILENAME, "wb+")

    while recieving_packets:
        readable, _, _ = select.select([sockIn], [], [], 1)

        if readable:
            print("recieved Pack")
            data, sender = sockIn.recvfrom(528)
            unpacked_packet = packets.unpack_packet(data)
            magicno, type, seqno, dataLen, data = unpacked_packet

            if magicno == int(MAGICNO, 0) and type == PTYPE_DATA and seqno == expected:

                ack_pack = packets.packet(seqno)
                ack_pack.set_ack()

                packed_packet = packets.pack_packet(ack_pack)

                expected ^= 1   #Switches between 0 and 1 with XOR Using bitwise operator

                if dataLen > 0: #data in packet
                    file_object.write(data)

                    try:
                        sockOut.send(packed_packet)
                    except:
                        error_count = raise_socket_error(socket_list, error_count)

                    else:
                        error_count = 0 #a packet has been successfully sent so we can reset errorcount

                else:   #datalen == 0
                    ack_pack = packets.packet(seqno)
                    ack_pack.set_ack()

                    packed_packet = packets.pack_packet(ack_pack)
                    try:
                        sockOut.send(packed_packet)
                    except:
                        error_count = raise_socket_error(socket_list, error_count)

                    else:
                        error_count = 0  # a packet has been successfully sent so we can reset errorcount

                    recieving_packets = False

            elif(magicno == int(MAGICNO, 0) and type == PTYPE_DATA and seqno != expected):

                ack_pack = packets.packet(seqno)
                ack_pack.set_ack()

                packed_packet = packets.pack_packet(ack_pack)
                try:
                    sockOut.send(packed_packet)
                except:
                    error_count = raise_socket_error(socket_list, error_count)

                else:
                    error_count = 0  # a packet has been successfully sent so we can reset errorcount

    file_object.close() #returns resources
    print("RECIEVED ALL DATA")
    exit()

if __name__ == '__main__':
    #makes it run automatically which is neat
    main()































