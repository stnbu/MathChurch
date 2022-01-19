# Math Church

tl;dr -- Drive your presentation entirely with subtitles interleaved with commands. Video: Manim, Audio: Google TTS.

This is a just-for-fun mathutainment project using [Manim](https://www.manim.community/) (of [3b1b](https://www.3blue1brown.com/) fame) as a graphics engine.

One goal is for all deliverables (lessens, math videos... sermons) to be Python scripts (text) only. The output can be improved in post, but the idea is for all of the content of the video and audio to be represented entirely in Python.

Because you can collaboratively and incrementally improve a text file. You can _not_ do this with a video file!

If subtitles are suboptimal for whatever reason, a human can easily just record and include (tbd) the audio files and re-run the script to incorporate the audio.

Join [the discord server](https://discord.gg/XTHcHc7N) and ask the friendly folks you meet there about how to contribute (plain old hanging out is encouraged also.)

# Install and run the demo

## tl;dr

* Have an Intel based Mac, [Big Sur or earlier](../../issues/3).
* Have a `latex` in your path
* Use Python v3.9.9 (or close)
* `pip install manim git+https://github.com/stnbu/MathChurch.git`
* `python3 /path/to/demo.py`

## Prereqs

### Mac (Intel? Pre-Monterey?)

So far I've only run this on Intel-based Big Sur machines. [Monterey in particular](../../issues/3) seems to maybe be problematic.

If you run/install on something else, please consider [sharing your experience](https://github.com/stnbu/MathChurch/issues/new) (good or bad).

You need to have the command `latex` in your shell's path. If you installed a latex package and `where latex` has no output, try closing and re-opening your terminal app (e.g. "Terminal").

Known to work is: [MacTex](https://www.tug.org/mactex/mactex-download.html)

### Python

[Manim](https://github.com/ManimCommunity/manim) is really the only dependency. If you can run Manim, you can run this stuff (minus maybe Google Cloud TTS).

I had problems trying to install Manim with the latest Big Sur-distributed `/usr/bin/python3`.

I instead have used the brew-distributed `python@3.9` and `python@3.10` packages, both with success.

Y.M.M.V.

As per [the manim installation instructions](https://docs.manim.community/en/stable/installation/macos.html#macos), you need to install the command line tools `py3cairo` and `ffmpeg` via brew.

> M1 processors will also need to have `cmake`, `pango`, and `scipy`.

### Software from this repo

This one is easy: `pip install manim git+https://github.com/stnbu/MathChurch.git`. The pip dependency system is bypassed for the moment so if you see `ImportError` messages, you probably need to install something. Manim is covered above. [Mutagen] and [GGG] together are needed to use _Google's_ text to speech.

`demo.py` simply uses the Mac's `say` command to write out TTS in the form of WAVE files. In other words: there are no dependencies for doing text-to-speech on a Mac. If you're a real minimalist, you can even just have use the "silence" TTS engine, which produces _roughly_ the right pauses for humans to read subtitles.

In addition to pip-installing this git repo, you might want a separate copy of the same repo, so you have a copy of `demo.py` (and others under `manual_testing`) that you can experiment with. To get a copy of this repo, just use git!

```
git clone https://github.com/stnbu/MathChurch.git
```

If your environment is working, you should be able to run _most_ of these:

```
ls -1 demo.py manual_testing/*.py
demo.py
manual_testing/baked_and_ripped.py
manual_testing/demo.py
manual_testing/run.py
manual_testing/simple.py
```

If you're feeling lucky and just want to install everything you might possibly need, you can just run

```
time pip install manim google-cloud-texttospeech mutagen GitPython
```

## If you want a script...

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

> ⚠ Note that caching has implications not yet understood [#3]
> Play it safe and `rm -rf ./media` between runs.

Having installed LaTeX, Manim, and this repo, you should be able to run `./demo.py` which will print the path to its output file: an MPEG-4 video file hopefully with both subtitles and audio.

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

## `tbob`

> ⚠ Note that (currently) you must manually `pip install GitPython` in order to run `tbob`.

`tbob` (`t`hree`b`lue`o`ne`b`rown) tries to make it possible to run [the scripts](https://github.com/3b1b/videos) used to create [3b1b](https://www.3blue1brown.com/) [content](https://www.youtube.com/c/3blue1brown).

It does this by:

1. Finding the commit in [3b1b/manim](https://github.com/3b1b/manim) that came just before the last commit of the video file you're trying to run (path is relative to [3b1b/videos](https://github.com/3b1b/videos) root.)
1. Checking out that commit in its own `3b1b/manim` repository.
1. Printing instructions to you to do the rest.

All of this happens under `~/tbob`. Take a look at the source at `tbob/__main__.py`.

You will find there is still more work to do. For example you might need to:

* `export PYTHONPATH=~/tbob/videos` Because there may be a module used in there!
* Find resources, like images (`pi_creature.svg`) and possibly `sed` the code to match.

Note that `tbob` thoroughly cleans its own repos under `~/tbob`, so don't put anything
valuable in there. You might consider having your own copy of [3b1b/videos](https://github.com/3b1b/videos) elsewhere to experiment
with.

If you just want to try tbob, it has minimal dependencies. You can just:

```
pip install git+https://github.com/stnbu/MathChurch.git
```

And you should have `tbob`!!

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
