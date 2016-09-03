"""
Sender part of assignment
#--Liz And Stefan--#
To run me type in the command line:
python sender.py portNum PortNum PortNum fileName
"""

#   python3 sender.py 7001 7000 8000 test.txt

import sys
import socket
import os.path #This is being used to check if file exists
import struct
import binascii
import packets
import select

MAX_BYTES = 512


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
        return fname
    else:
        print("File: " + fname + " does not exist.")
        exit()

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
        SIN = checkPort(sys.argv[0])
        SOUT = checkPort(sys.argv[1])
        CSIN = checkPort(sys.argv[2])
        FILENAME = checkFile(sys.argv[3])

    return  SIN, SOUT, CSIN, FILENAME


def read_file_data(file_obj):
    """reads a max amount of data into a buffer"""
    return file_obj.read(MAX_BYTES)


def  return_resources(socket_list, file_object):
    """closes sockets and file
        giving memory back to system"""
    for sockets in socket_list:
        sockets.close()
    file_object.close()


def raise_socket_error(socket_list, file_object, ERROR_COUNT):
    """if connection to a socket is refused an error is raised
        will wait 10 times and then time out"""
    if ERROR_COUNT >10:

        print()
        print("----------------------------------------")
        print("-----------Connection timeout-----------")
        print("----------Program will now exit---------")
        print("----------------------------------------")
        print()

        return_resources(socket_list, file_object)
        exit()
    else:
        print()
        print("---connection refused, trying again-----")
        print()

    return ERROR_COUNT+1

def main():
    """main function for sender
        sends a file to channel"""


    SIN, SOUT, CSIN, FILENAME = get_params()

    sockOut = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sockOut.bind(('127.0.0.1', SOUT))
    sockOut.connect(('127.0.0.1', CSIN))

    sockIn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockIn.bind(('127.0.0.1', SIN))

    next = 0
    exitFlag = False

    file_object = open(FILENAME, "rb")


    all_packets_count  = 0
    ack_packet_count = 0
    socket_list = [sockOut, sockIn]
    ERROR_COUNT = 0

    print()
    while not exitFlag:
        current_string = read_file_data(file_object)
        if len(current_string) == 0:
            current_packet = packets.packet(next, len(current_string), current_string)
            exitFlag = True
            print("seding final packet")

        elif len(current_string) > 0:
            current_packet = packets.packet(next, len(current_string), current_string)

        encoded_packet = packets.pack_packet(current_packet)

        has_response = False
        while not has_response:
            try:
                sockOut.send(encoded_packet) #sendencoded packet
                all_packets_count += 1
            except:
                ERROR_COUNT = raise_socket_error(socket_list, file_object, ERROR_COUNT)


            else:
                ERROR_COUNT = 0 #a packet has been successfully sent so we can reset errorcount

            print("------------Sending Packet--------------")


            readable, _, _ = select.select([sockIn], [], [], 1)

            if readable:
                data = sockIn.recv(528)
                has_response = True
                print()

                print("------------recieved ack Pack-----------")
                ack_packet_count +=1

        next ^= 1 #Switches between 0 and 1 with XOR Using bitwise operator


    print("Total num packets sent: ", all_packets_count)
    print("Successful packets:     ", ack_packet_count  )
    return_resources(socket_list, file_object)
    exit()

if __name__ == '__main__':
    main()




































