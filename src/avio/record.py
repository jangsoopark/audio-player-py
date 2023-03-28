import sounddevice as sd
import threading


class Record(threading.Thread):

    def __init__(self, device, sample_rate, channels, block_size, buffer):
        super(Record, self).__init__()
        self.event = threading.Event()
        self.device = device
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.channels = channels
        self._current_frame = 0
        self.buffer = buffer

    def run(self) -> None:
        stream = sd.InputStream(
            device=self.device, samplerate=self.sample_rate, channels=self.channels,
            callback=self.callback, blocksize=self.block_size, dtype='int16'
        )
        with stream:
            self.event.wait()

    def callback(self, input_data, _frames, _time, status):
        if status:
            print(status)
        # print(_frames, input_data.shape)
        self.buffer.put_nowait({
            'frames': _frames,
            'data': input_data
        })
