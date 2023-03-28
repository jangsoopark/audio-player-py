from network.protocols import packet
import socketserver
import socket
import numpy as np
import queue


class TCPHandler(socketserver.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        server.clients[client_address] = request
        super(TCPHandler, self).__init__(request, client_address, server)

    def setup(self):
        pass

    def handle(self):
        while True:
            data = self._receive()
            if not data or data is None:
                self._empty_packet()
                continue
            self._packet_received(data)
            header, body = data
            for k, v in self.server.clients.items():
                if (socket.inet_ntoa(header.address), header.port) == k:
                    continue

                v.send(packet.Encode.header(header.packet_id, 2, 3, header.data_size, header.address, header.port))
                v.send(packet.Encode.body(body.frames, body.data))

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
