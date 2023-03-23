from avio import audio
from avio import record
from avio import play

import sounddevice as sd
import soundfile as sf
import threading
import queue

import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('main')
logger.setLevel(level=logging.DEBUG)

parser = argparse.ArgumentParser(description='ㄹㅇㅋㅋ')
parser.add_argument('--list-device', action='store_true', help='sequence configuration path')
parser.add_argument('--sequence-config', type=str, default='', help='sequence configuration path')
parser.add_argument('--sample-rate', type=float, help='sampling rate of audio device')
parser.add_argument('--window', type=float, default=200, metavar='DURATION',
                    help='visible time slot (default: %(default)s ms)')
parser.add_argument('--down-sample', type=int, default=10, metavar='N',
                    help='display every Nth sample (default: %(default)s)')
parser.add_argument('--channels', type=int, default=1, nargs='*', metavar='CHANNEL',
                    help='input channels to plot (default: the first)')

parser.add_argument('--block-size', type=int, default=1136, nargs='*', metavar='CHANNEL',
                    help='input channels to plot (default: the first)')

parser.add_argument('--interval', type=float, default=30,
                    help='minimum time between plot updates (default: %(default)s ms)')
parser.add_argument('--input-device', type=int, default=1, help='input device (numeric ID or substring)')
parser.add_argument('--output-device', type=int, default=4, help='output device (numeric ID or substring)')
args = parser.parse_args()


def main():
    if args.list_device:
        print(sd.query_devices())

    q = queue.Queue()

    recorder = record.Record(
        device=args.input_device, sample_rate=args.sample_rate, channels=args.channels,
        block_size=args.block_size, buffer=q
    )

    player = play.Play(
        device=args.output_device, sample_rate=args.sample_rate, channels=args.channels,
        block_size=args.block_size, buffer=q
    )
    recorder.start()
    player.start()


if __name__ == '__main__':
    main()
