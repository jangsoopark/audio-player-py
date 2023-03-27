from network.protocols import packet
from avio import record

import numpy as np
import socket
import queue

import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('client')
logger.setLevel(level=logging.DEBUG)

parser = argparse.ArgumentParser(description='ㄹㅇㅋㅋ')
parser.add_argument('--threading', action='store_true', help='sequence configuration path')
parser.add_argument('--host', type=str, default='localhost', help='sequence configuration path')
parser.add_argument('--port', type=int, default=12345, help='sequence configuration path')
parser.add_argument('--input-device', type=int, default=1, help='input device (numeric ID or substring)')
parser.add_argument('--sample-rate', type=float, default=16000, help='sampling rate of audio device')
parser.add_argument('--channels', type=int, default=1, nargs='*', metavar='CHANNEL',
                    help='input channels to plot (default: the first)')
args = parser.parse_args()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((args.host, args.port))
        address, port = s.getsockname()
        q = queue.Queue()
        recorder = record.Record(
            device=args.input_device, sample_rate=args.sample_rate, channels=args.channels,
            buffer=q
        )
        recorder.start()

        packet_id = 0

        while True:
            try:
                data = q.get_nowait()
                body = packet.Encode.body(data['frames'], data['data'].tobytes())
                header = packet.Encode.header(packet_id, 2, 3, len(body), socket.inet_aton(address), port)
                s.send(header)
                s.send(body)
                packet_id += 1
            except queue.Empty:
                pass


if __name__ == '__main__':
    main()
