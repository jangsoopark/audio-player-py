import sounddevice as sd
import numpy as np
import threading
import queue


class Play(threading.Thread):

    def __init__(self, device, sample_rate, channels, block_size, buffer, status):
        super(Play, self).__init__()
        self.event = threading.Event()
        self.device = device
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.channels = channels
        self._current_frame = 0
        self.buffer = buffer
        self.status = status

    def run(self) -> None:
        stream = sd.OutputStream(
            device=self.device, samplerate=self.sample_rate, channels=self.channels,
            callback=self.callback, blocksize=self.block_size, dtype='int16',
            never_drop_input=False
        )
        with stream:
            self.event.wait()

    def callback(self, output_data, _frames, _time, status):
        if status:
            self.status.put_nowait(status)
        try:
            d = self.buffer.get_nowait()
            # print(_frames, d['frames'])
            assert _frames == d['frames']
            data = d['data']
        except queue.Empty as _:
            output_data.fill(0)
            return
        # except AssertionError:
        #     return

        if len(data) < len(output_data):
            output_data[:len(data)] = data
            output_data[len(data):].fill(0)
            raise sd.CallbackStop
        output_data[:] = data[:_frames, :]
