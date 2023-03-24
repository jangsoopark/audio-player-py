from typing import NamedTuple
import struct

struct_header = struct.Struct('!4I')

header_size = 32
body_size = 4


class Header(NamedTuple):
    packet_id: int
    command: int
    status: int
    data_size: int


class Body(NamedTuple):
    frames: int
    data: bytes


class Encode(object):

    @staticmethod
    def header(packet_id: int, command: int, status: int, data_size: int) -> bytes:
        return struct_header.pack(
            packet_id, command, status, data_size
        )

    @staticmethod
    def body(frames: int, data: bytes) -> bytes:
        return struct.pack(f'!I{len(data)}s', frames, data)


class Decode(object):

    @staticmethod
    def header(data: bytes) -> Header:
        return Header(*struct_header.unpack(data))

    @staticmethod
    def body(data: bytes) -> Body:
        return Body(*struct.unpack(f'!I{len(data) - body_size}s', data))
