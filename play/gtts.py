"""Speech Therapy

* https://github.com/googleapis/python-texttospeech
* https://cloud.google.com/text-to-speech/docs/libraries
"""
import re, hashlib, os

def get_normalized_input_hash(input):
    """Crude, heavyhanded normalization of input. Return its hash.

    Text to speech is currently done by GCS. Runaway requests are bad.
    """
    result = re.sub(r'[^\w ]|[_\d]', '', input)
    result = re.sub(r'\s+', ' ', result).strip().lower()
    # some hash
    return hashlib.sha224(result.encode()).hexdigest()


def get_audio_cache_path(hash):
    path = os.path.join('media', 'audio', hash + ".mp3")  # MP33333
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path

def get_audio_bytes(input, bytes_getter):
    hash = get_normalized_input_hash(input)
    path = get_audio_cache_path(hash)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return f.read() # um

    audio_bytes = bytes_getter(input)
    with open(path, 'wb') as f:
        f.write(audio_bytes)
    return audio_bytes

if __name__ == "__main__":

    assert (
        get_normalized_input_hash("my frog has fleas.") ==
        get_normalized_input_hash(" My \t frog $ has _ -  fleas! \t ")
    )

    def _test_bytes_getter(input):
        return input.encode()

    def _exceptional_bytes_get(input):
        raise AssertionError

    bytes1 = get_audio_bytes("hi planet", _test_bytes_getter)
    bytes2 = get_audio_bytes("hi planet!!", _exceptional_bytes_get)

    assert bytes1 == bytes2
