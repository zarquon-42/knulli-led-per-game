# LED Settings per Game Proof of Concept (POC)

This script leverages the LED Daemon from [chrizzo-hb](https://github.com/chrizzo-hb)
to set the analog joystick LED on the Anbernic RG40XX series devices
on a per game bases within [Knulli](https://knulli.org/).

## Installation

Log into the device via ssh and execute the following command:

```bash
curl -sL https://raw.githubusercontent.com/zarquon-42/knulli-led-per-game/refs/heads/main/install.sh | bash
```

## Usage

The `led_game_colour.sh` script is triggered on a games launch and looks
for an `.led` file within the `/userdata/roms/<system>/led` folder.  The
`.led` file will match the rom file name and contains a RGB tuple which
is then passed on to LED Daemon.  Obviously this service needs to be
active.

The script automatically creates missing `.led` files based in the artwork.
If no artwork exists the files will need to be manually created. You can
manually create the files.

If the automatically created colour is not desired you can manually edit the
`.led` file.

## Uninstall

Log into the device via ssh and execute the following command:

```bash
rm /userdata/system/scripts/led_game_colour.sh
```

## Development Notes

This uses the library `Pillow` and `numpy` which are already installed within
Knulli but you may need to create a virtual environment on your dev machine.
