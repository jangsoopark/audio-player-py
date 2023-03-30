from typing import NamedTuple
import struct

struct_header = struct.Struct('!h4I4sI')

prefix = 0x1234
header_size = 26
body_size = 4


class Header(NamedTuple):
    prefix: int
    packet_id: int
    command: int
    status: int
    data_size: int
    address: bytes
    port: int


class Body(NamedTuple):
    frames: int
    data: bytes


class Encode(object):

    @staticmethod
    def header(packet_id: int, command: int, status: int, data_size: int, address: bytes, port: int) -> bytes:
        return struct_header.pack(
            prefix, packet_id, command, status, data_size, address, port
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
