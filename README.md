# Math Church

tl;dr -- Drive your presentation entirely with subtitles interleaved with commands. Video: Manim, Audio: Google TTS.

This is a just-for-fun mathutainment project using [Manim](https://www.manim.community/) (of [3b1b](https://www.3blue1brown.com/) fame) as a graphics engine.

One goal is for all deliverables (lessens, math videos... sermons) to be Python scripts (text) only. The output can be improved in post, but the idea is for all of the content of the video and audio to be represented entirely in Python.

Because you can collaboratively and incrementally improve a text file. You can _not_ do this with a video file!

If subtitles are suboptimal for whatever reason, a human can easily just record and include (tbd) the audio files and re-run the script to incorporate the audio.

Join [the discord server](https://discord.gg/XTHcHc7N) and ask the friendly folks you meet there about how to contribute (plain old hanging out is encouraged also.)

# Install and run the demo

The main attraction is `demo.py`. You can run `demo.py` by following these instructions.

> ⚠ Assumptions:
>   1. You are running a recent OSX on Intel Mac hardware (M1: keep reading)
>   2. The "python3" on your system is Python 3.9.9 (or close)

Note that the `/usr/bin/python3` (3.8.2) bundled with Big Sur `11.6.1 20G224` gave me lots of trouble. YMMV. I've been using the `python@3.9` distributed by brew.

As per [the manim installation instructions](https://docs.manim.community/en/stable/installation/macos.html#macos), you need to install the command line tools `py3cairo` and `ffmpeg` via brew.

> M1 processors will also need to have `cmake`, `pango`, and `scipy`.

## Install

These commands should work. Reflect and refine to taste.

```
brew install py3cairo ffmpeg
[ $(uname -m) = "arm64" ] && brew install cmake pango scipy # untested
python3 -m venv ~/mc_demo_venv
source ~/mc_demo_venv/bin/activate
pip -qqq install manim google-cloud-texttospeech mutagen # the latter two only for GCSTTS
pip install git+https://github.com/stnbu/MathChurch.git # or "editable mode" if you prefer
```

## Run

Once your laptop cools down, you should be able to run `./demo.py` which will print the path to its output file: an MPEG-4 video file hopefully with both subtitles and audio.

The output will look something like this:

```
$ ./demo.py
Manim Community v0.13.1

[01/10/22 09:59:45] INFO Writing "h(u*v)=h(u) \odot h(v)" to media/Tex/000.tex scene_file_writer.py:749
 . . . lines of logs . . .
                        File ready at '/cwd/media/videos/480p15/Scene.mp4'
 . . . lines of logs . . .
                             Played 9 animations
```

`Scene.mp4` is a video that should look and sound something like this:

[![Subs 2 Video](http://img.youtube.com/vi/_c5xLnW9Eo0/0.jpg)](http://www.youtube.com/watch?v=_c5xLnW9Eo0 "Subs 2 Video")

If you're feeling adventurous...

1. Set up Google Cloud Services Text-to-Speech
1. Export the `GOOGLE_APPLICATION_CREDENTIALS` environment variable with the path to
your credentials JSON file
1. Modify `demo.py` thusly:

```diff
@@ -39,6 +39,6 @@
 config.quality = "low_quality"
 scene = Scene()
 # you may also try: silence_tts, google_tts
-player = Player(scene, lecture, local_tts)
+player = Player(scene, lecture, google_tts)
 player.play()
 scene.render()
```

## Hey, where do you think you're going with this thing?

I'll try to summarize/reign in the/my own chaos:

Mini-roadmap:

1. Find a "dev-mode" solution to TTS:
   * Get `pyttsx3` or similar to work. It might end up being more straight-
   forward to call `say` with `Subproc` (or whatever it's called now) and print
   the filename (only) for return value.
   [Here](https://github.com/nateshmbhat/pyttsx3/issues/177#issuecomment-1008033309)
   is a comment from me about the bug-in-question.
   [[UPDATE](https://bugs.python.org/issue30077) -- yay, everyone just upgrade to
   the latest python. UPDATE2 -- one can use `.wav` output.
   e.g. `--data-format=LEI32@22050 ... -o foo.wav`]
   * _And also_/_Or_ whip up a better-quality "subs-duration-estimator" (e.g.
   divide word count by a reasonable words-per-second value...tweak as needed).
1. Get such that you can easily consume e.g.
[this](https://discord.com/channels/927656471599149117/927656472203112461/929421225686622249)
or similar, coordinating with author.
1. Finish reasonable "subtitle chunk" abstraction, possibly with
[this](https://github.com/stnbu/MathChurch/blob/4ea56db05e62f0a1d1ce8c3ce0ab4085d8c6fd59/presenter/the_subtitle_class_poc.py) as inspiration.
1. Whatever the input format, get some things in the queue:
   * Negative numbers/subtraction/symbolism in math.
   * Continuous fractions representation of $$\pi$$.
   * Maybe steal some of Grant's output and re-do with subs-to-speech in place
   of narrator.
