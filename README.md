# Math Church

tl;dr -- Drive your presentation entirely with subtitles interleaved with commands. Video: Manim, Audio: Google TTS.

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

As of fab59a85a2e142f065b4921f9fc076caa6b67267, the output of `python play/presenter.py` looks like this (Youtube video link):

[![Subs 2 Video](http://img.youtube.com/vi/_c5xLnW9Eo0/0.jpg)](http://www.youtube.com/watch?v=_c5xLnW9Eo0 "Subs 2 Video")

## Hey, where do you think you're going with this thing?

I'll try to summarize/reign in the/my own chaos:

Mini-roadmap:

1. Find a "dev-mode" solution to TTS:
  * Get `pyttsx3` or similar to work. It might end up being more straight forward to call `say` with `Subproc` (or whatever it's called now) and print the filename (only) for return value. [Here](https://github.com/nateshmbhat/pyttsx3/issues/177#issuecomment-1008033309) is a comment from me about the bug-in-question.
  * _And also_/_Or_ whip up a better-quality "subs-duration-estimator" (e.g. divide word count by a reasonable words-per-second value...tweak as needed).
1. Get such that you can easily consume e.g. [this](https://discord.com/channels/927656471599149117/927656472203112461/929421225686622249) or similar, coordinating with author.
1. Finish reasonable "subtitle chunk" abstraction, possibly with [this](https://github.com/stnbu/MathChurch/blob/4ea56db05e62f0a1d1ce8c3ce0ab4085d8c6fd59/presenter/the_subtitle_class_poc.py) as inspiration.
1. Whatever the input format, get some things in the queue:
  * Negative numbers/subtraction/symbolism in math.
  * Continuous fractions representation of $$\pi$$.
  * Maybe steal some of Grant's output and re-do with subs-to-speech in place of narrator.
