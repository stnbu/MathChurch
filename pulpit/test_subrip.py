import os
from pulpit.subrip import *

import unittest


class SubsTests(unittest.TestCase):
    def test_sub_rip_output(self):
        srf = SubRipFile(
            SubRipChunk(0, 1, "Hello, world!"),
        )
        got = srf.get_file_contents()
        expected = "1\n00:00:00,000 --> 00:00:01,000\nHello, world!\n\n"
        assert got == expected

    def test_sub_rip_roundtrip(self):
        srt_file_name = "/tmp/we_want_a_safe_temp_file.srt"
        srf = SubRipFile(
            SubRipChunk(1, 9.257, "Somebody set up us the bomb."),
        )
        srf.write_to(srt_file_name)
        got = ""
        expected = "1\n00:00:01,000 --> 00:00:09,256\nSomebody set up us the bomb.\n\n"
        with open(srt_file_name) as f:
            got = f.read()
        assert got == expected
