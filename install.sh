#!/bin/bash

# Download generate scripts and set permissions
echo -n "Downloading Scripts..."
curl \
    --silent \
    --location \
    https://raw.githubusercontent.com/zarquon-42/knulli-led-per-game/refs/heads/main/generate_game_colour.py \
    --output /opt/generate_game_colour.py && \
curl \
    --silent \
    https://raw.githubusercontent.com/zarquon-42/knulli-led-per-game/refs/heads/main/led_game_colour.sh \
    --output /userdata/system/scripts/led_game_colour.sh && \
echo " Complete" && \
echo -n "Setting Permissions..." && \
chmod +x /opt/generate_game_colour.py && \
chmod +x /userdata/system/scripts/led_game_colour.sh && \
echo " Complete" && \
echo -n "Making changes permanent..." && \
batocera-save-overlay >/dev/null && \
echo " Complete" && \
echo "" && \
echo "Installation Complete" && \
echo "" && \
echo "
Notes:

Starting a game should change the led to
reflect the game art work.

You can manually edit the colours by editing
or creating an .led file in the folder
/userdata/roms/<system>/led folder
"