from network.protocols import packet
from avio import play

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
parser.add_argument('--output-device', type=int, default=4, help='output device (numeric ID or substring)')
parser.add_argument('--sample-rate', type=float, default=16000, help='sampling rate of audio device')
parser.add_argument('--block-size', type=int, default=1024, help='the number of frames per second')
parser.add_argument('--channels', type=int, default=1, nargs='*', metavar='CHANNEL',
                    help='input channels to plot (default: the first)')
args = parser.parse_args()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((args.host, args.port))
        address, port = s.getsockname()
        q = queue.Queue()
        player = play.Play(
            device=args.output_device, sample_rate=args.sample_rate, channels=args.channels,
            buffer=q, block_size=args.block_size
        )
        player.start()

        while True:
            try:
                d = s.recv(packet.header_size)
                header = packet.Decode.header(d)
                if header.prefix != packet.prefix:
                    continue
                d = s.recv(packet.body_size + header.data_size)
                body = packet.Decode.body(d)

                q.put_nowait({
                    'frames': body.frames,
                    'data': np.frombuffer(body.data, dtype=np.int16).reshape(-1, 1)
                })
            except queue.Empty:
                pass
            except ConnectionAbortedError:
                break
            except ConnectionResetError:
                break
            except KeyboardInterrupt:
                break
        player.event.set()
        player.join()


if __name__ == '__main__':
    main()
