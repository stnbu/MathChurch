from collections import namedtuple


from manim import logger

SubRipChunk = namedtuple("SubRipChunk", ["appear", "disappear", "text"])


class SubRipFile:
    def __init__(self, *chunks):
        self._chunks = []
        for chunk in chunks:
            self.add(chunk)

    def to_offset(self, seconds):
        assert seconds <= 60 * 60 * 24
        milliseconds = int(seconds % 1 * 1000)
        seconds = int(seconds)
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        string = "%02d:%02d:%02d,%03d" % (hours, minutes, seconds, milliseconds)
        return string

    def add(self, chunk):
        assert isinstance(chunk, SubRipChunk)
        if len(self._chunks) > 0:
            previous_disappear = self._chunks[-1].disappear
            this_appear = chunk.appear
            if previous_disappear > this_appear:
                raise ValueError(
                    "Cannot add chunk whose appear time is before "
                    "previous chunk's disappear time (%d > %d)."
                    % (previous_disappear, this_appear)
                )
        self._chunks.append(chunk)

    def get_file_contents(self):
        results = ""
        for index, chunk in enumerate(self._chunks):
            results += ("%d\n" "%s --> %s\n" "%s\n\n") % (
                index + 1,
                self.to_offset(chunk.appear),
                self.to_offset(chunk.disappear),
                chunk.text,
            )
        return results

    def write_to(self, path):
        with open(path, "w") as f:
            f.write(self.get_file_contents())
        logger.error("SubRip file written to: %s" % path)


if __name__ == "__main__":
    srf = SubRipFile(
        SubRipChunk(0, 1, "my first text"),
        SubRipChunk(2, 3.3, "my second text"),
        SubRipChunk(3.9, 5.1234, "my\n..build-up"),
        SubRipChunk(6, 7, "the BIG crachendo"),
        SubRipChunk(8, 9.54321, "my lame let-down"),
        SubRipChunk(10, 1000, "fin"),
    )
    print(srf.get_file_contents())
    srf.write_to("/tmp/foo.srt")
