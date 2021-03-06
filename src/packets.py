import struct
MAX_BYTES = 512
MAGICNO = hex(0x497E)
PTYPE_DATA = 0
PTYPE_ACK = 1

class packet:
    """Packet class as defined by instructions"""
    def __init__(self, seqno, dataLen=0, data=b'', type=PTYPE_DATA, magicno=MAGICNO):
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
        return out_string

    def set_ack(self):
        self.type = PTYPE_ACK


def magicNoCheck(magicno):
    """Cechkes if magic numbe is 0x497E"""
    return magicno == int(MAGICNO, 0)

def pack_packet(current_packet):
    """Packs packet into binary data"""
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
    """Unpacks binary data from packet"""
    pack_format = 'I I I I {0}s'.format(len(packed_packet)-16)
    my_struct = struct.Struct(pack_format)
    unpacked_packet = my_struct.unpack(packed_packet)
    return unpacked_packet
