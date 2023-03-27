from network.server import handler
import socketserver

import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('main')
logger.setLevel(level=logging.DEBUG)

parser = argparse.ArgumentParser(description='ㄹㅇㅋㅋ')
parser.add_argument('--threading', action='store_true', help='sequence configuration path')
parser.add_argument('--host', type=str, default='localhost', help='sequence configuration path')
parser.add_argument('--port', type=int, default=12345, help='sequence configuration path')
args = parser.parse_args()


def main():
    tcp_server = socketserver.ThreadingTCPServer if args.threading else socketserver.TCPServer

    with tcp_server((args.host, args.port), handler.TCPHandler) as s:
        s.allow_reuse_address = True
        s.allow_reuse_port = True
        s.clients = {}
        s.serve_forever()


if __name__ == '__main__':
    main()
