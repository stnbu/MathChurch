"""Speech Therapy

* https://github.com/googleapis/python-texttospeech
* https://cloud.google.com/text-to-speech/docs/libraries
* https://www.w3.org/TR/speech-synthesis/ (with SSML reference)

Note that we assume "mp3 throughout". It's hard-coded here and there.
"""

import re, hashlib, os, logging
from google.cloud import texttospeech


def get_local_speech_from_text(input):
    import pyttsx3, random, tempfile, time
    logging.warning("You are using the 'development' TTS service. It might break your laptop!")
    path = os.path.join(tempfile.gettempdir(), str(random.randint(1e11, 1e12-1)) + ".wav")
    print(path)
    engine = pyttsx3.init()
    engine.save_to_file(input, path)
    engine.runAndWait()
    time.sleep(1)
    with open(path, "rb") as f:
        bytes = f.read()
    #os.remove(path)
    return bytes


def get_google_speech_from_text(input):
    logging.warning(
        "Performing TTS operation using Google Cloud Text-to-speech. This may cost actual money."
    )
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=input)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response.audio_content


def get_normalized_input_hash(input):
    """Crude, heavy-handed normalization of input. Return its hash.

    Text to speech is currently done by GCS. Runaway requests are bad.
    """
    result = re.sub(r"[^\w ]|[_\d]", "", input)
    result = re.sub(r"\s+", " ", result).strip().lower()
    # some hash
    return hashlib.sha224(result.encode()).hexdigest()


def get_audio_cache_path(hash, driver, format):
    path = os.path.join("media", "audio", driver, hash + "." + format)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


def get_audio_bytes(input, bytes_getter):
    hash = get_normalized_input_hash(input)
    path = get_audio_cache_path(hash)
    if os.path.exists(path):
        logging.info("cache hit for %s" % hash)
        return open(path, "rb").read(), path
    logging.info("cache miss for %s" % hash)
    audio_bytes = bytes_getter(input)
    with open(path, "wb") as f:
        f.write(audio_bytes)
    return audio_bytes, path


if __name__ == "__main__":

    import pyttsx3

    corpus = "what if I made this a totally unusual but very long sentence of great hatred, but then just totally changed subjects I cannot wonder what if there was never an end. You know, what if I made a new sentence."


    engine = pyttsx3.init()#("espeak", debug=True)
    engine.save_to_file(corpus, '/tmp/xblarggg3.wav')
    engine.runAndWait()
    import sys; sys.exit(0)

    #import ipdb; ipdb.set_trace()
    bytes = get_local_speech_from_text(corpus)
    with open('/tmp/ggg.wav', 'wb') as f:
        f.write(bytes)


    assert get_normalized_input_hash("my frog has fleas.") == get_normalized_input_hash(
        " My \t frog $ has _ -  fleas! \t "
    )

    def _test_bytes_getter(input):
        return input.encode()

    def _exceptional_bytes_get(input):
        raise AssertionError

    bytes1, path1 = get_audio_bytes("hi planet", _test_bytes_getter)
    bytes2, path2 = get_audio_bytes("hi planet!!", _exceptional_bytes_get)

    assert bytes1 == bytes2
    assert path1 == path2

    # # This works, but it will consume API resources (your money).
    # text = "Hello, World!"
    # the_bytes = get_audio_bytes(text, get_google_speech_from_text)
    # with open("test.mp3", "wb") as f:  # should be in your cache too.
    #     f.write(the_bytes)
