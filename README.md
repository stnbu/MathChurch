# Math Church

tl;dr -- Drive your presentation entirely with subtitles interleaved with commands. Video: Manim, Audio: GTTS.

This is a just-for-fun mathutainment project using [Manim](https://www.manim.community/) (of [3b1b](https://www.3blue1brown.com/) fame) as a graphics engine.

One goal is for all deliverables (lessens, math videos... sermons) to be Python scripts (text) only. The output can be improved in post, but the idea is for all of the content of the video and audio to be represented entirely in Python.

Because you can collaboratively and incrementally improve a text file. You can _not_ do this with a video file!

If subtitles are suboptimal for whatever reason, a human can easily just record and include (tbd) the audio files and re-run the script to incorporate the audio.

Join [the discord server](https://discord.gg/XTHcHc7N) and ask the friendly folks you meet there about how to contribute (plain old hanging out is encouraged also.)

# State-of-the-Church

You can run

```
python play/presenter.py
```

After satisfying all prerequisites.

Hints:

* Signing up for Google Text-to-Speech is a pain in the ass. Good luck!
* Other than that, manim is probably the most challenging thing. See their [excellent docs](https://docs.manim.community/en/stable).
* Holler. Submit an issue. Open a PR. and/or [Join the Discord](https://discord.gg/XTHcHc7N).

As of [this version](https://github.com/stnbu/MathChurch/blob/fab59a85a2e142f065b4921f9fc076caa6b67267/play/presenter.py), the output of `python play/presenter.py` looks like this:

[![Subs 2 Video](http://img.youtube.com/vi/_c5xLnW9Eo0/0.jpg)](http://www.youtube.com/watch?v=_c5xLnW9Eo0 "Subs 2 Video")
