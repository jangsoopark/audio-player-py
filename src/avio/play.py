import sounddevice as sd
import threading
import queue


class Play(threading.Thread):

    def __init__(self, device, sample_rate, channels, block_size, buffer):
        super(Play, self).__init__()
        self.event = threading.Event()
        self.device = device
        self.sample_rate = sample_rate
        self.channels = channels
        self.block_size = block_size
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
        assert _frames == self.block_size
        if status:
            print(status)
        try:
            data = self.buffer.get_nowait()
        except queue.Empty as _:
            return

        if len(data) < len(output_data):
            output_data[:len(data)] = data
            output_data[len(data):].fill(0)
            raise sd.CallbackStop
        output_data[:] = data
