"""Speech Therapy

* https://github.com/googleapis/python-texttospeech
* https://cloud.google.com/text-to-speech/docs/libraries
* https://www.w3.org/TR/speech-synthesis/ (with SSML reference)

Note that we assume "mp3 throughout". It's hard-coded here and there.
"""

from manim import logger

import re, hashlib, os

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
    command = ["say", "--data-format=LEI16", "-v", "Alex", input, "-o", path]
    logger.info("Running: Popen(%s)" % (command))
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    logger.info("Popen(%s) exitied with status %d" % (command, proc.returncode))
    logger.info("STDOUT>%s" % out)
    logger.info("STDERR>%s" % err)
    return None, path

if __name__ == "__main__":

    assert get_normalized_input_hash("my frog has fleas.") == get_normalized_input_hash(
        " My \t frog $ has _ -  fleas! \t "
    )
