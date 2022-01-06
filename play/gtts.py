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
    result = re.sub(r'\s+', ' ', result).strip()
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

def _test_bytes_getter(input):
    return input.encode()


bts = get_audio_bytes("hi planet", _test_bytes_getter)

import ipdb; ipdb.set_trace()

from mutagen.mp3 import MP3
audio = MP3("output.mp3")
print(audio.info.length)


from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()

synthesis_input = texttospeech.SynthesisInput(text="Hello, World!")

voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)


with open("output.mp3", "wb") as out:
    out.write(response.audio_content)


