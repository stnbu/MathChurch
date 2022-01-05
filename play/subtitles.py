#!/usr/bin/env python3

from pathlib import PosixPath
from manim import *


class Subtitles(Scene):
    """"""

    # def construct(self):
    #     subs = Text("People of Earth!!")
    #     self.add(subs)
    #     self.wait(10)


class SubFrame(Scene):
    def construct(self):
        vg = VGroup()
        self.add(vg)


class ClickArgs:
    def __init__(self, args):
        for name in args:
            setattr(self, name, args[name])

    def _get_kwargs(self):
        return list(self.__dict__.items())

    def __eq__(self, other):
        if not isinstance(other, ClickArgs):
            return NotImplemented
        return vars(self) == vars(other)

    def __contains__(self, key):
        return key in self.__dict__

    def __repr__(self):
        return str(self.__dict__)


def do_config():
    args = {
        "preview": True,
        "quality": "l",
        "file": PosixPath("play/subtitles.py"),
        "scene_names": ("Subtitles",),
        "config_file": None,
        "custom_folders": None,
        "disable_caching": None,
        "flush_cache": None,
        "tex_template": None,
        "verbosity": None,
        "notify_outdated_version": None,
        "enable_gui": None,
        "gui_location": None,
        "fullscreen": None,
        "enable_wireframe": None,
        "force_window": False,
        "dry_run": False,
        "output_file": None,
        "zero_pad": None,
        "write_to_movie": None,
        "media_dir": None,
        "log_dir": None,
        "log_to_file": None,
        "from_animation_number": None,
        "write_all": None,
        "format": None,
        "save_last_frame": None,
        "resolution": None,
        "frame_rate": None,
        "renderer": None,
        "use_opengl_renderer": None,
        "use_webgl_renderer": None,
        "webgl_renderer_path": None,
        "save_pngs": None,
        "save_as_gif": None,
        "save_sections": None,
        "transparent": False,
        "use_projection_fill_shaders": None,
        "use_projection_stroke_shaders": None,
        "progress_bar": None,
        "show_in_file_browser": None,
        "jupyter": None,
    }
    click_args = ClickArgs(args)
    config.digest_args(click_args)


if __name__ == "__main__":
    do_config()

    subs = Subtitles()

    text = Text("People of Earth!!")
    subs.add(text)
    subs.wait(3)
    subs.remove(text)

    text = Text("Look at this!!")
    subs.add(text)
    subs.wait(3)
    subs.remove(text)

    text = Text("(gestures rudely)")
    subs.add(text)
    subs.wait(3)
    subs.remove(text)

    subs.render()

    # scene = Subtitles()

    # scene.render()
