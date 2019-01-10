import struct

def parse(origin, port, data):
    if origin == "server" or port == 3333:
        return
    print("Message from {} on port {}: {}".format(origin, port, data.hex()))
    packet_id = struct.unpack(">H", data[:2])[0]
    print(hex(packet_id))


def get_packet_id(data):
    return data.hex()[:4]


"""
Packet dump from jumping:
6d76 05fa13c7 6fd69ec6 4ef72345 d0fa4918 0000 0000
6d76 05fa13c7 6fd69ec6 85042545 d0fa4918 0000 0000
6d76 05fa13c7 6fd69ec6 7fc32545 d0fa4918 0000 0000
6d76 05fa13c7 6fd69ec6 29572645 d0fa4918 0000 0000
6d76 05fa13c7 6fd69ec6 5a312645 d0fa4918 0000 0000
6d76 05fa13c7 6fd69ec6 00c22545 d0fa4918 0000 0000
6d76 05fa13c7 6fd69ec6 f5092545 d0fa4918 0000 0000
6d76 05fa13c7 6fd69ec6 d5ff2345 d0fa4918 0000 0000
6d76 05fa13c7 6fd69ec6 a5ac2245 d0fa4918 0000 0000
6d76 05fa13c7 6fd69ec6 1c092145 d0fa4918 0000 0000
                       

Packet dump from moving:
6d76 727e13c7 fdf09fc6 d8c81b45 e6fa8918 0000 7f7f
6d76 298c13c7 65c69fc6 69c51b45 e6fa8918 0000 7f7f
6d76 198f13c7 b8889fc6 acc41b45 e6fa8918 0000 7f00
6d76 6f8013c7 7f519fc6 54c81b45 e6fa8918 0000 7f81
6d76 2b6813c7 95419fc6 65ce1b45 e6fa8918 0000 0081
6d76 0f4f13c7 b9569fc6 aed41b45 e6fa8918 0000 0081
6d76 993a13c7 c8879fc6 87d71b45 e6fa8918 0000 8181
6d76 7e3613c7 26c99fc6 87d71b45 e6fa8918 0000 817f
6d76 e74613c7 19f39fc6 3dd71b45 e6fa8918 0000 817f
6d76 1d6113c7 bcfe9fc6 aed01b45 e6fa8918 0000 007f

Packet dump from moving camera:
6d76 4f7a13c7 eeec9fc6 60ca1b45 740d81fe 0000 0000
6d76 4f7a13c7 eeec9fc6 60ca1b45 ddf8f340 0000 0000
6d76 4f7a13c7 eeec9fc6 60ca1b45 91164643 0000 0000
6d76 4f7a13c7 eeec9fc6 60ca1b45 f0168510 0000 0000
6d76 4f7a13c7 eeec9fc6 60ca1b45 70f43734 0000 0000
6d76 4f7a13c7 eeec9fc6 60ca1b45 88094f58 0000 0000
6d76 4f7a13c7 eeec9fc6 60ca1b45 0f1ff127 0000 0000
6d76 4f7a13c7 eeec9fc6 60ca1b45 e401d621 0000 0000
6d76 4f7a13c7 eeec9fc6 60ca1b45 cd07344b 0000 0000

Packet format:
[2 byte packet id][4 byte x coords][4 byte y coords][4 byte z coords][4 byte camera movement][2 byte ?][2 byte key input]
"""