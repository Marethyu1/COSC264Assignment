"""
Channel part of assignment
#--Liz And Stefan--#

To run me type in the command line:
python channel.py portNum PortNum PortNum PortNum S(in) R(in) P
"""
#   python3 channel.py 8000 8001 8003 8002 7001 9000 0.1
import sys
import socket
import select
import packets
import random



def exit():
    """Exits the program displaying a message"""
    print("Program will now exit\n")
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

def checkProbability(p):
    """checks to make sure the probability enteed is a float in the range [0,1)
        exits if there is an error
        returns probability P """
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
    """gets all of the parameters from the command line
        exits if wrong amount of arguments are entered
        checks to ensure input is correct
        reutrns port numbers and P"""
    if len(sys.argv) != 8:
        print("\nWrong amount of command line arguments entered")
        exit()
    else:    
        sys.argv = sys.argv[1:] #chops off the name of the program
        CSIN = checkPort(sys.argv[0])
        CSOUT = checkPort(sys.argv[1])
        CRIN = checkPort(sys.argv[2])
        CROUT = checkPort(sys.argv[3])
        SIN = checkPort(sys.argv[4])
        RIN = checkPort(sys.argv[5])
        P = checkProbability(sys.argv[6])

        
    return  CSIN, CSOUT, CRIN, CROUT, SIN, RIN, P
    
def can_send(P):
    """generates a uniformly distrubuted number between 0 and 1
        drops packet if u < P
        returns true if packet can be sent"""
    to_send = False
    u = random.uniform(0, 1)
    if u >= P:
        to_send =  True
    return to_send

def  return_resources(socket_list):
    """closes sockets and file
        giving memory back to system"""
    for sockets in socket_list:
        sockets.close()

def raise_socket_error(socket_list, ERROR_COUNT):
    """If connection resets """
    if ERROR_COUNT >10:
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

    return ERROR_COUNT+1

def raise_listen_error(socket_list, LISTENING_FLAG):
    """Raises error if has been listening too long"""
    if LISTENING_FLAG > 20:

        print()
        print("----------------------------------------")
        print("--------No responses in a while---------")
        print("------ has been listening too long -----")
        print("---------Program will now exit----------")
        print("----------------------------------------")
        print()

        return_resources(socket_list)
        exit()






def main():
    """main fuction for channel
        makes four sockets then listens waiting for a packet from sender or receiver
        randomly decides to drop packet or not
        if packet it isnt dropped it passes it through"""

    CSIN, CSOUT, CRIN, CROUT, SIN, RIN, P = get_params()

    sockCSOut = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sockCSOut.bind(('127.0.0.1', CSOUT))
    sockCSOut.connect(('127.0.0.1', SIN))  # So we don't have to specify where we send to

    sockCSIn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockCSIn.bind(('127.0.0.1', CSIN))


    sockCROut = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockCROut.bind(('127.0.0.1', CROUT))
    sockCROut.connect(('127.0.0.1', RIN))  # So we don't have to specify where we send to

    sockCRIn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockCRIn.bind(('127.0.0.1', CRIN))

    socket_list = [sockCROut, sockCRIn, sockCSIn, sockCSOut]
    ERROR_COUNT = 0
    LISTENING_FLAG = 0

    while True:
        readable, _, _ = select.select([sockCSIn, sockCRIn], [], [], 1)

        print("\nlistening\n")
        if len(readable) == 0:
            LISTENING_FLAG += 1
            if LISTENING_FLAG > 20:
                raise_listen_error(socket_list, LISTENING_FLAG)

        else:
            LISTENING_FLAG = 0 #reset listening time
            for sockets in readable:

                if sockets is sockCSIn:
                    data, addr = sockCSIn.recvfrom(528)
                    unpacked_packet = packets.unpack_packet(data)
                    magicno, type, seqno, dataLen, byte_data = unpacked_packet

                    if packets.magicNoCheck(magicno):
                        print("recieved Datapack...")
                        if can_send(P):
                            print("sending Datapack")
                            try:
                                sockCROut.send(data)
                            except:
                                ERROR_COUNT = raise_socket_error(socket_list, ERROR_COUNT)

                        else:
                            print("PACKET FAILED TO SEND")

                if sockets is sockCRIn:
                    data, addr = sockCRIn.recvfrom(528)
                    unpacked_packet = packets.unpack_packet(data)
                    magicno, type, seqno, dataLen, byte_data = unpacked_packet

                    if packets.magicNoCheck(magicno):
                        print("recieved ackPacket")
                        if can_send(P):
                            # now we can send the packet
                            print("sending AckPack")
                            try:
                                sockCSOut.send(data)
                            except:
                                ERROR_COUNT = raise_socket_error(socket_list ,ERROR_COUNT)

                        else:
                            print("PACKET FAILED TO SEND")


if __name__ == '__main__':
    #makes it run automatically which is neat
    main()