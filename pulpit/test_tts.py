"""NOTE:

These test may:
* Write to disk
* Execute subprocesses
* Use paid API resources (e.g. GCS)
"""

import os
from pulpit.tts import *

import unittest


class TTSTests(unittest.TestCase):
    def test_get_audio_path_signature(self):
        got = get_audio_path("Hello, world!", "test_engine", "tstfmt")
        expected = "media/audio/test_engine/8552d8b7a7dc5476cb9e25dee69a8091290764b7f2a64fe6e78e9568.tstfmt"
        assert got == expected
        assert os.path.exists(os.path.dirname(got))
