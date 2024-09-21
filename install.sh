#!/bin/bash

# Download generate scripts and set permissions
echo "Downloading Scripts..."
curl \
    --silent \
    --location \
    https://raw.githubusercontent.com/zarquon-42/knulli-led-per-game/refs/heads/main/generate_game_colour.py \
    --output /opt/generate_game_colour.py && \
curl \
    --silent \
    https://raw.githubusercontent.com/zarquon-42/knulli-led-per-game/refs/heads/main/led_game_colour.sh \
    --output /userdata/system/scripts/led_game_colour.sh && \
echo "Setting Permissions..." && \
chmod +x /opt/generate_game_colour.py && \
chmod +x /userdata/system/scripts/led_game_colour.sh && \
echo "Making changes permanent..." && \
batocera-save-overlay >/dev/null && \
echo Done
