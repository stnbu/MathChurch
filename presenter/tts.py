"""Text to speech
"""

import hashlib, os
from manim import logger

def silent_tts(input):
    import wave
    #"5292000" # total byte count silent 30s clip.
    #"176400" # bytes-per-second of silence (nulls)
    length = 30
    sample_rate = 44100
    wav = wave.Wave_write("/tmp/test30_.wav")
    wav.setnchannels(1)
    wav.setsampwidth(1)
    wav.setframerate(sample_rate)
    wav.writeframes(b'\x00' * sample_rate * length)
    wav.close()

silent_tts("")
import sys; sys.exit(0)

def get_audio_path(input, engine, format):
    hash = hashlib.sha224(input.encode()).hexdigest()
    path = os.path.join("media", "audio", engine, hash + "." + format)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path

def local_tts(input):
    import subprocess
    import wave
    import contextlib

    path = get_audio_path(input, "local", "wav")
    command = ["say", "--data-format=LEI16", "-v", "Alex", input, "-o", path]
    logger.debug("Running: Popen(%s)" % (command))
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    logger.debug("Popen(%s) exitied with status %d" % (command, proc.returncode))
    logger.debug("STDOUT>%s" % out)
    logger.debug("STDERR>%s" % err)
    length = 0.0
    with contextlib.closing(wave.open(path, "r")) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        length = frames / float(rate)
    return path, length


def google_tts(input):
    from mutagen.mp3 import MP3
    from google.cloud import texttospeech

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
    path = get_audio_path(input, "google", "mp3")
    with open(path, "wb") as f:
        f.write(response.audio_content)
    return path, MP3(path).info.length
