"""Speech Therapy

* https://github.com/googleapis/python-texttospeech
* https://cloud.google.com/text-to-speech/docs/libraries
* https://www.w3.org/TR/speech-synthesis/ (with SSML reference)

Note that we assume "mp3 throughout". It's hard-coded here and there.
"""

from manim import logger

import re, hashlib, os #, logging
from google.cloud import texttospeech

def get_google_speech_from_text(input):
    logger.warning(
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


def get_audio_cache_path(input, engine, format):
    hash = get_normalized_input_hash(input)
    path = os.path.join("media", "audio", engine, hash + "." + format)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path

def osx_alex_say_subproc(input):
    import subprocess


    path = get_audio_cache_path(input, "alex", "wav")

    if os.path.exists(path):
        logger.info("cache hit for %s" % path)
        return None, path
    logger.info("cache miss for %s" % path)

    command = ["say", "--data-format=LEI32@22050", "-v", "Alex", input, "-o", path]
    #print(' '.join(command))
    #import sys; sys.exit(0)
    logger.info("Running: Popen(%s)" % (command))
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    logger.info("Popen(%s) exitied with status %d" % (command, proc.returncode))
    logger.info("STDOUT>%s" % out)
    logger.info("STDERR>%s" % err)
    return None, path

#corpus = "This is a long, annoying sentence that will make 'Alex' sweat. Here is the next sentence. Can Alex ask questions? " * 3
#
#p = osx_alex_say_subproc(corpus)
#rint(p)
#
#import sys; sys.exit(0)


def get_audio_bytes(input, bytes_getter):
    hash = get_normalized_input_hash(input)
    path = get_audio_cache_path(hash)
    if os.path.exists(path):
        logger.info("cache hit for %s" % hash)
        return open(path, "rb").read(), path
    logger.info("cache miss for %s" % hash)
    audio_bytes = bytes_getter(input)
    with open(path, "wb") as f:
        f.write(audio_bytes)
    return audio_bytes, path


if __name__ == "__main__":

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
