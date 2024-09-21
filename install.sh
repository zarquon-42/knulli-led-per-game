#!/bin/bash

# Download generate scripts and set permissions
curl --silent https://raw.githubusercontent.com/zarquon-42/knulli-led-per-game/refs/heads/main/generate_game_colour.py --output /opt/generate_game_colour.py
curl --silent https://raw.githubusercontent.com/zarquon-42/knulli-led-per-game/refs/heads/main/led_game_colour.sh --output /userdata/system/scripts/led_game_colour.sh
chmod +x /opt/generate_game_colour.py
chmod +x /userdata/system/scripts/led_game_colour.sh

# Save the changes
batocera-save-overlay
