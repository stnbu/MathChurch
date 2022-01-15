import io
import builtins

circle = """
<svg height="100" width="100">
  <circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red" />
</svg>
"""


def open_mock_svg(*args, **kwargs):
    if len(args) < 1:
        raise ValueError
    path = args[0]
    if (len(args) > 1 and "w" not in args[1]) or (
        "mode" in kwargs and "w" not in kwargs["mode"]
    ):
        if path[-4:].lower() == ".svg":
            return io.StringIO(circle)
    return io.open(*args, **kwargs)
