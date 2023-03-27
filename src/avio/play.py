import sounddevice as sd
import threading
import queue


class Play(threading.Thread):

    def __init__(self, device, sample_rate, channels, buffer):
        super(Play, self).__init__()
        self.event = threading.Event()
        self.device = device
        self.sample_rate = sample_rate
        self.channels = channels
        self._current_frame = 0
        self.buffer = buffer

    def run(self) -> None:
        stream = sd.OutputStream(
            device=self.device, samplerate=self.sample_rate, channels=self.channels,
            callback=self.callback, finished_callback=self.event.set
        )
        with stream:
            self.event.wait()

    def callback(self, output_data, _frames, _time, status):
        # print(output_data.shape, output_data.dtype)
        if status:
            print(status)
        try:
            d = self.buffer.get_nowait()
            assert _frames == d['frames']
            data = d['data']
        except queue.Empty as _:
            return

        if len(data) < len(output_data):
            output_data[:len(data)] = data
            output_data[len(data):].fill(0)
            raise sd.CallbackStop
        output_data[:] = data
