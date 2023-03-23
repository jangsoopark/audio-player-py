import numpy as np
import librosa
import wave


def padding16(buf):
    size = len(buf)
    return buf + b'\x00' * (16 - size % 16)


def load_audio(path):
    if path.endswith('wav'):
        return librosa.load(path)

    # the extension is pcm
    if not path.endswith('pcm'):
        raise Exception('Unsupported Extension')

    with open(path, mode='rb') as f:
        buf = padding16(f.read())

        pcm = np.frombuffer(buf, dtype=np.int16)
        wav = librosa.util.buf_to_float(pcm, n_bytes=2)
        return wav, 16000
