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

_tbob_helper "$1"

. ~/tbob/venv/bin/activate

# The manim repo likely changed its state. So we do this every time:
cd ~/tbob/manim
pip install -e .

cd ~/tbob/videos
PYTHONPATH=. manim-render -l --config_file="$CONFIG_FILE" "$@"
