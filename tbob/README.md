
# How I ran [`manim-render _2021/newton_fractal.py Thanks`](https://github.com/3b1b/videos/blob/f5da1924e49b34dcc586cde6eb36b507ce341479/_2021/newton_fractal.py)

The script `_2021/newton_fractal.py` requires a few things:

* SVG `pi_creature`. I just grabbed any old SVG pi symbol. And copied it to:
  * `/tmp/pi_svg/gracious.svg`
  * `/tmp/pi_svg/happy.svg`
* Knowledge of how to import `videos/manim_imports_ext.py`. I set the `PYTHONPATH` env var thusly:
  * `export PYTHONPATH=~/tbob/vidoes`
  
The whole process looked like this:

```
. ~/tbob/venv/bin/activate
cd ~/tbob/videos
export PYTHONPATH=~/tbob/videos
manim-render _2021/newton_fractal.py Thanks
```

**However**, I had to make some changes to the `~/tbob/manim` and `~/tbob/videos` repos. Note that _you
cannot do this_ unless you disable the cleanup in `tbob/__main__.py`. You just need to comment some lines. Make sure you're changing the file that python is actually using (the one that `tbob` will import). The changes are:

```diff
diff --git a/tbob/__main__.py b/tbob/__main__.py
index bedcb78..78d0e4f 100644
--- a/tbob/__main__.py
+++ b/tbob/__main__.py
@@ -55,10 +55,10 @@ def get_repo(path, origin=None):
             raise Exception("%s does not exist and no remote URL was supplied" % path)
         repo = Repo.clone_from(url=origin, to_path=path)
     else:
-        clean(path)
+        #clean(path)
         repo = Repo(path)
-        repo.heads.master.checkout()  # what about (...) main?
-        repo.remote().pull()
+        #repo.heads.master.checkout()  # what about (...) main?
+        #repo.remote().pull()
     return repo
 
 
```

Below are changes I also made to the repos under `~/tbob`:

## Changes to `~/tbob/manim`

```diff
diff --git a/manimlib/mobject/mobject.py b/manimlib/mobject/mobject.py
index 1050c3ee..2ae85247 100644
--- a/manimlib/mobject/mobject.py
+++ b/manimlib/mobject/mobject.py
@@ -252,7 +252,7 @@ class Mobject(object):
         if isinstance(value, slice):
             GroupClass = self.get_group_class()
             return GroupClass(*self.split().__getitem__(value))
-        return self.split().__getitem__(value)
+        return self.split().__getitem__(0)
 
     def __iter__(self):
         return iter(self.split())
```

## Changes to `~/tbob/videos`

```
diff --git a/custom/characters/pi_creature.py b/custom/characters/pi_creature.py
index ffc9d64..2d6c8a5 100644
--- a/custom/characters/pi_creature.py
+++ b/custom/characters/pi_creature.py
@@ -19,11 +19,11 @@ from manimlib.utils.space_ops import normalize
 PI_CREATURE_SCALE_FACTOR = 0.5
 
 LEFT_EYE_INDEX = 0
-RIGHT_EYE_INDEX = 1
-LEFT_PUPIL_INDEX = 2
-RIGHT_PUPIL_INDEX = 3
-BODY_INDEX = 4
-MOUTH_INDEX = 5
+RIGHT_EYE_INDEX = 0
+LEFT_PUPIL_INDEX = 0
+RIGHT_PUPIL_INDEX = 0
+BODY_INDEX = 0
+MOUTH_INDEX = 0
 
 
 class PiCreature(SVGMobject):
@@ -210,7 +210,7 @@ class PiCreature(SVGMobject):
 
     def is_flipped(self):
         return self.eyes.submobjects[0].get_center()[0] > \
-            self.eyes.submobjects[1].get_center()[0]
+            self.eyes.submobjects[0].get_center()[0]
 
     def blink(self):
         eye_parts = self.eye_parts
diff --git a/custom_config.yml b/custom_config.yml
index 0249a69..7b14f4b 100644
--- a/custom_config.yml
+++ b/custom_config.yml
@@ -1,12 +1,12 @@
 directories:
   mirror_module_path: True
-  output: "/Users/grant/Dropbox/3Blue1Brown/videos"
-  raster_images: "/Users/grant/Dropbox/3Blue1Brown/images/raster"
-  vector_images: "/Users/grant/Dropbox/3Blue1Brown/images/vector"
-  pi_creature_images: "/Users/grant/Dropbox/3Blue1Brown/images/pi_creature/svg"
-  sounds: "/Users/grant/Dropbox/3Blue1Brown/sounds"
-  data: "/Users/grant/Dropbox/3Blue1Brown/data"
-  temporary_storage: "/Users/grant/Dropbox/3Blue1Brown/manim_cache"
+  output: "/tmp/grant/videos"
+  raster_images: "/tmp/grant/images/raster"
+  vector_images: "/tmp/grant/images/vector"
+  pi_creature_images: "/tmp/pi_svg"
+  sounds: "/tmp/grant/sounds"
+  data: "/tmp/grant/data"
+  temporary_storage: "/tmp/grant/manim_cache"
 universal_import_line: "from manim_imports_ext import *"
 # tex:
 #   executable: "xelatex -no-pdf"
```