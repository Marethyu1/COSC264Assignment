
MAX_BYTES = 512
MAGICNO = hex(0x497E)
PTYPE_DATA = 0
PTYPE_ACK = 1

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
