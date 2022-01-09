"""Text to speech
"""

import hashlib, os
from manim import logger

def get_audio_path(input, engine, format):
    hash = hashlib.sha224(input.encode()).hexdigest()
    path = os.path.join("media", "audio", engine, hash + "." + format)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path

def osx_alex_say_subproc(input):
    import subprocess
    path = get_audio_path(input, "alex", "wav")
    command = ["say", "--data-format=LEI16", "-v", "Alex", input, "-o", path]
    logger.debug("Running: Popen(%s)" % (command))
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    logger.debug("Popen(%s) exitied with status %d" % (command, proc.returncode))
    logger.debug("STDOUT>%s" % out)
    logger.debug("STDERR>%s" % err)
    return path

def get_google_speech_from_text(input):
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
    
    path = get_audio_path(input, "gcstts", "mp3")
    with open(path, 'wb') as f:
        f.write(response.audio_content)
    return path
