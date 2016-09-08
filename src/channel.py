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
        csin = checkPort(sys.argv[0])
        csout = checkPort(sys.argv[1])
        crin = checkPort(sys.argv[2])
        crout = checkPort(sys.argv[3])
        sin = checkPort(sys.argv[4])
        rin = checkPort(sys.argv[5])
        P = checkProbability(sys.argv[6])

        
    return  csin, csout, crin, crout, sin, rin, P
    
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

def raise_socket_error(socket_list, error_count):
    """If connection resets """
    if error_count >5:
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

    return error_count + 1

def raise_listen_error(socket_list, listening_flag):
    """Raises error if has been listening too long"""
    if listening_flag > 5:
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

    csin, csout, crin, crout, sin, rin, P = get_params()

    sockCSOut = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sockCSOut.bind(('127.0.0.1', csout))
    sockCSOut.connect(('127.0.0.1', sin))  # So we don't have to specify where we send to

    sockCSIn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockCSIn.bind(('127.0.0.1', csin))


    sockCROut = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockCROut.bind(('127.0.0.1', crout))
    sockCROut.connect(('127.0.0.1', rin))  # So we don't have to specify where we send to

    sockCRIn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockCRIn.bind(('127.0.0.1', crin))

    socket_list = [sockCROut, sockCRIn, sockCSIn, sockCSOut]
    error_count = 0
    listening_flag = 0

    while True:
        readable, _, _ = select.select([sockCSIn, sockCRIn], [], [], 1)

        print("\nlistening\n")
        if len(readable) == 0:
            listening_flag += 1
            if listening_flag > 20:
                raise_listen_error(socket_list, listening_flag)

        else:
            listening_flag = 0 #reset listening time
            for sockets in readable:

                if sockets is sockCSIn: #if data is rome channel
                    data, addr = sockCSIn.recvfrom(528)
                    unpacked_packet = packets.unpack_packet(data)
                    magicno, type, seqno, dataLen, byte_data = unpacked_packet

                    if packets.magicNoCheck(magicno):
                        print("recieved Datapack...")
                        if can_send(P):
                            print("forwarding Datapack")
                            try:
                                sockCROut.send(data)
                            except:
                                error_count = raise_socket_error(socket_list, error_count)
                        else:
                            print("PACKET FAILED TO SEND")

                if sockets is sockCRIn: #if data is from reciever
                    data, addr = sockCRIn.recvfrom(528)
                    unpacked_packet = packets.unpack_packet(data)
                    magicno, type, seqno, dataLen, byte_data = unpacked_packet

                    if packets.magicNoCheck(magicno):
                        print("recieved ackPacket")
                        if can_send(P):
                            # now we can send the packet
                            print("Forwarding AckPack")
                            try:
                                sockCSOut.send(data)
                                print("Ackpack sent")
                            except:
                                error_count = raise_socket_error(socket_list ,error_count)

                        else:
                            print("ACKPACKET FAILED TO SEND")


if __name__ == '__main__':
    #makes it run automatically which is neat
    main()