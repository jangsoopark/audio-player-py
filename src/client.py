from network.protocols import packet
import numpy as np
import socket

import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('client')
logger.setLevel(level=logging.DEBUG)

parser = argparse.ArgumentParser(description='ㄹㅇㅋㅋ')
parser.add_argument('--threading', action='store_true', help='sequence configuration path')
parser.add_argument('--host', type=str, default='localhost', help='sequence configuration path')
parser.add_argument('--port', type=int, default=12345, help='sequence configuration path')
args = parser.parse_args()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((args.host, args.port))
        data = np.zeros((416, 1)).tobytes()
        body = packet.Encode.body(416, data)
        header = packet.Encode.header(1, 2, 3, len(body))
        s.send(header)
        print(header, packet.Decode.header(header))
        s.send(body)


if __name__ == '__main__':
    main()
