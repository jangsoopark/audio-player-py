from avio import audio
from avio import record
from avio import play

import sounddevice as sd
import queue

import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('main')
logger.setLevel(level=logging.DEBUG)

parser = argparse.ArgumentParser(description='ㄹㅇㅋㅋ')
parser.add_argument('--list-device', action='store_true', help='sequence configuration path')
parser.add_argument('--sequence-config', type=str, default='', help='sequence configuration path')
parser.add_argument('--input-device', type=int, default=1, help='input device (numeric ID or substring)')
parser.add_argument('--output-device', type=int, default=4, help='output device (numeric ID or substring)')
parser.add_argument('--sample-rate', type=float, default=16000, help='sampling rate of audio device')
parser.add_argument('--channels', type=int, default=1, nargs='*', metavar='CHANNEL',
                    help='input channels to plot (default: the first)')

args = parser.parse_args()


def main():
    if args.list_device:
        print(sd.query_devices())

    q = queue.Queue()

    recorder = record.Record(
        device=args.input_device, sample_rate=args.sample_rate, channels=args.channels,
        buffer=q
    )

    player = play.Play(
        device=args.output_device, sample_rate=args.sample_rate, channels=args.channels,
        buffer=q
    )
    recorder.start()
    player.start()


if __name__ == '__main__':
    main()
