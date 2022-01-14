#!/bin/sh -ue

TEMP=$(mktemp -d)

echo "Temporary files under here: ${TEMP}"

CONFIG_FILE="${TEMP}/config.yml"

cat > "$CONFIG_FILE" << EOF
directories:
  mirror_module_path: True
  output: "${TEMP}/videos"
  raster_images: "${TEMP}/images/raster"
  vector_images: "${TEMP}/images/vector"
  pi_creature_images: "/tmp/pi_svg"
  sounds: "${TEMP}/sounds"
  data: "${TEMP}/data"
  temporary_storage: "${TEMP}/manim_cache"
EOF

. ~/tbob/venv/bin/activate
cd ~/tbob/videos
PYTHONPATH=. manim-render -l --config_file="$CONFIG_FILE" "$@"

# ManimGL [32mv1.3.0[0m
# usage: manim-render [-h] [-w] [-s] [-l] [-m] [--hd] [--uhd] [-f] [-g] [-i]
#                     [-t] [-q] [-a] [-o] [--finder] [--config]
#                     [--file_name FILE_NAME] [-n START_AT_ANIMATION_NUMBER]
#                     [-e LINENO] [-r RESOLUTION] [--frame_rate FRAME_RATE]
#                     [-c COLOR] [--leave_progress_bars] [--video_dir VIDEO_DIR]
#                     [--config_file CONFIG_FILE] [-v] [--log-level LOG_LEVEL]
#                     [file] [scene_names ...]
# 
# positional arguments:
#   file                  path to file holding the python code for the scene
#   scene_names           Name of the Scene class you want to see
# 
# optional arguments:
#   -h, --help            show this help message and exit
#   -w, --write_file      Render the scene as a movie file
#   -s, --skip_animations
#                         Save the last frame
#   -l, --low_quality     Render at a low quality (for faster rendering)
#   -m, --medium_quality  Render at a medium quality
#   --hd                  Render at a 1080p
#   --uhd                 Render at a 4k
#   -f, --full_screen     Show window in full screen
#   -g, --save_pngs       Save each frame as a png
#   -i, --gif             Save the video as gif
#   -t, --transparent     Render to a movie file with an alpha channel
#   -q, --quiet
#   -a, --write_all       Write all the scenes from a file
#   -o, --open            Automatically open the saved file once its done
#   --finder              Show the output file in finder
#   --config              Guide for automatic configuration
#   --file_name FILE_NAME
#                         Name for the movie or image file
#   -n START_AT_ANIMATION_NUMBER, --start_at_animation_number START_AT_ANIMATION_NUMBER
#                         Start rendering not from the first animation, butfrom
#                         another, specified by its index. If you passin two
#                         comma separated values, e.g. "3,6", it will endthe
#                         rendering at the second value
#   -e LINENO, --embed LINENO
#                         Takes a line number as an argument, and resultsin the
#                         scene being called as if the line `self.embed()`was
#                         inserted into the scene code at that line number.
#   -r RESOLUTION, --resolution RESOLUTION
#                         Resolution, passed as "WxH", e.g. "1920x1080"
#   --frame_rate FRAME_RATE
#                         Frame rate, as an integer
#   -c COLOR, --color COLOR
#                         Background color
#   --leave_progress_bars
#                         Leave progress bars displayed in terminal
#   --video_dir VIDEO_DIR
#                         Directory to write video
#   --config_file CONFIG_FILE
#                         Path to the custom configuration file
#   -v, --version         Display the version of manimgl
#   --log-level LOG_LEVEL
#                         Level of messages to Display, can be DEBUG / INFO /
#                         WARNING / ERROR / CRITICAL
