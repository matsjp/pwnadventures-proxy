import struct
from enum import Enum

global_packet_id = None
global_packet_origin = None

def parse(origin, port, data):
    global global_packet_id
    global global_packet_origin
    packet_id = struct.unpack(">H", data[:2])[0]
    global_packet_id = packet_id
    global_packet_origin = origin
    if packet_id == 0 or port == 3333 or packet_id == PacketType.Position.value or packet_id == PacketType.Jump.value:
        return
    #print("Message from {} on port {}: {}".format(origin, port, data.hex()))
    handler.get(packet_id, h_noop)(data[2:])


def h_noop(data):
    global global_packet_id
    global global_packet_origin
    print("Unknown {} packet: {} {}".format(global_packet_origin, format(global_packet_id, 'x'), data.hex()))


def h_position(data):
    x, y, z = struct.unpack("fff", data[0:3*4])
    print("Position: {:.2f} / {:.2f} / {:.2f}".format(x, y, z))


def h_jump(data):
    print("Jump: {}".format(data.hex()[6:len(data.hex()) - 16]))


def h_server_talk(data):
    print("Server talk: {}".format(data.hex()))


def h_client_talk(data):
    print("Client talk: {}".format(data.hex()))

def h_client_initiate_conversation(data):
    print("Client initiate conversation: {}".format(data.hex()))

def h_server_end_conversation(data):
    print("Server end conversation: {}".format(data.hex()))

def h_sprint_toggle(data):
    print("Sprint toggle: {}".format(data.hex()))

def h_enemy_position(data):
    print("Enemy position: {}".format(data.hex()))

handler = {
    0x6d76: h_position,
    0x6a70: h_jump,
    0x2373: h_server_talk,
    0x233e: h_client_talk,
    0x6565: h_client_initiate_conversation,
    0x2366: h_server_end_conversation,
    0x726e: h_sprint_toggle,
    0x7073: h_enemy_position
}


def get_packet_id(data):
    return data.hex()[:4]


class PacketType(Enum):
    """"
    [2 byte packet id:0x6d76]
    [4 byte x coords]
    [4 byte y coords]
    [4 byte z coords]
    [4 byte camera movement]
    [2 byte ?]
    [2 byte key input]"""
    Position = int(0x6d76)
    """
    [2 byte packet id:0x6a70]
    [1 byte space key press]
    [2 byte position packet id?: 0x6d76]
    [4 byte x coords]
    [4 byte y coords]
    [4 byte z coords]
    [4 byte camera movement]
    [2 byte ?]
    [2 byte key input]"""
    Jump = int(0x6a70)
    Server_talk = int(0x2373)
    Client_talk = int(0x233e)
    Client_initiate_conversation = int(0x6565)
    Server_end_conversation = int(0x2366)
    Sprint_toggle = int(0x726e)
    Enemy_position = int(0x7073)

"""

2 byte packet id     1 byte keypress                constant
                     1 for press, 0 for release     Position packet?  x            y              z            camera position       ?      Key pressed
Jump:                   00                          6d76        687150c7        58eb60c7        c5719444    78f55108            0000        0000
Jump:                   01                          6d76        687150c7        58eb60c7        e8da8144    78f55108            0000        0000
Jump:                   00                          6d76        687150c7        58eb60c7        a6d79344    78f55108            0000        0000
                                                                044f50c7        722361c7        f5bf8544    54f3dc19            0000        0000
                        00                          6d76        2f991bc7        5fec9ac6        d41a2745    dff26b8a            0000        0000
"""