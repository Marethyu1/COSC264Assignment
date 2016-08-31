""" Demonstrating the socket libraries in Python 3.
    To run this program, use the following:
        python3 sockets.py --server <server_port>
    and
        python3 sockets.py --client <client_port> <server_port>
    in two different terminal windows, to see them communicate.
    Always start the server first. The client can then be run
    as many times as you wish.
    Although this file has both the client and server together,
    this is not the recommended approach. Normally, they would
    be two separate programs/files. They are combined here
    for convenience.

    Aaron Stockdill, COSC264, 2016
"""


import argparse  # for command line arguments
import socket  # for sockets
import datetime  # for getting the date in a pretty way
import select  # for listening nicely on sockets


# Both are running on localhost, so we use this address.
IP = '127.0.0.1'


def server(port):
    """ Run the socket server.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # sets IP, UDP
    sock.bind((IP, port))  # Claim the port for the server to use

    while True:
        data, sender = sock.recvfrom(1024)  # Get some data, blocking
        if data == b'request-time':  # b is for bytes, strings are too fancy
            now = datetime.datetime.now().strftime("%I:%M:%S%p on %B %d, %Y")
            sock.sendto(bytes(now, 'utf8'), sender)  # Reply back to sender with bytes
        else:
            print("BAD PACKET")



def client(my_port, their_port):
    """ Run the socket client.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP, my_port))
    sock.connect((IP, their_port))  # So we don't have to specify where we send to
    sock.send(b'request-time')  # Remember, bytes not strings
    readable, _, _ = select.select([sock], [], [], 2)  # Last number is timeout
    if readable: # Make sure that we can now read from the socket
        # readable is a list containing only 'sock',
        # so we could replace 'sock' with 'readable[0]'
        # If we were waiting on multiple things, we should loop over readable
        data, addr = sock.recvfrom(1024)
        print(data.decode('utf8'))  # Actually get a string again...
    else:
        print("TIMEOUT")



if __name__ == '__main__':
    # This isn't so important, basically it checks which mode and gets port numbers
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--server", action="store_true",
                       help="start the socket server")
    group.add_argument("--client", action="store_true",
                       help="start the socket client")
    parser.add_argument("client_port", type=int, nargs='?',
                        help="the port the client connects through")
    parser.add_argument("server_port", type=int,
                        help="the port the server listens on")
    args = parser.parse_args()
    if args.server:
        server(args.server_port)
    elif args.client:
        if not args.client_port:
            raise parser.error("if in client mode, client_port is required")
        client(args.client_port, args.server_port)






