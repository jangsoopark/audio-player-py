import numpy as np
from network.protocols import packet
import socketserver


class TCPHandler(socketserver.BaseRequestHandler):

    def setup(self):
        pass

    def handle(self):
        while True:
            data = self._receive()
            if not data or data is None:
                self._empty_packet()
                break
            self._packet_received(data)

    def finish(self):
        pass

    def _receive(self):
        try:
            d = self.request.recv(packet.header_size)
            header = packet.Decode.header(d)
            d = self.request.recv(packet.body_size + header.data_size)
            body = packet.Decode.body(d)
            return header, body
        except Exception as e:
            print(f'{self.address} {e}')
            return None

    @property
    def address(self):
        _addr, _port = self.request.getpeername()
        return f'{_addr}:{_port}'

    # log message function
    def _empty_packet(self):
        pass

    def _packet_received(self, data):
        pass
