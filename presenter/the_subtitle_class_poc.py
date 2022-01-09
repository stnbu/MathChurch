#!/usr/bin/env python

import hashlib
from presenter import *

class C:

    def __init__(self, text):
        self.text = text

    def _get_under_boundaries(self):
        """Return the underscore indexes in pairs. Input

          "my _dog_ has _fleas_!"

        returns

          [(3, 7), (13, 19)]
        """
        under_indexes = [i for (i, c) in enumerate(self.text) if c == '_']
        if len(under_indexes) % 2 == 1:
            raise ValueError
        pairs = []
        for i in range(0, len(under_indexes), 2):
            pairs.append((under_indexes[i], under_indexes[i + 1]))
        return pairs

    def get_normalized_hash(self):
        "the hash of the normalized view"
        return hashlib.sha224(self.get_normalized_view().encode()).hexdigest()

    def get_subitle_view(self):
        "what will be printed on the screen"
        needs_close = False
        result = ""
        for c in self.text:
            if c == '_':
                if not needs_close:
                    result += tag_open
                    needs_close = False
                else:
                    result += tag_close
            else:
                result += c
        return result

        result = []
        tag_open = "<emphasis>"
        tag_close = "</emphasis>"
        for pair in get_x():
            open, close = pair
            before = self.text[:open]
            during = self.text[open + 1:close]
            after = self.text[close + 1:]
            result.extetnd([before, tag_open, during, tag_close])

    def get_normalized_view(self):
        """Strip out some stuff, lower case, collapse whitespace, etc.
        The goal is to not allow "adding a comma" to result in calling the
        possibbly "expensive" TTS engine.
        """
        result = re.sub(r"[^\w ]|[_\d]", "", self.text)
        return re.sub(r"\s+", " ", result).strip().lower()

    def get_tts_view(self):
        "what the tts engine will take as input"


if __name__ == "__main__":

    sub = C("  my _dog_ has _fleas_!  ")
    assert sub._get_under_boundaries() == [(5, 9), (15, 21)]
    assert sub.get_normalized_view() == "my dog has fleas"
    assert sub.get_normalized_hash() == "98df6e36bb6790cee3ccf0e458c1dbdf07f44b275d68b4792b8453af"
