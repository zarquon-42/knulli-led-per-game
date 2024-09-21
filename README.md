# LED Settings per Game Proof of Concept (POC)

This is a proof of concept for setting the thumb LED on a per game bases
within [Knulli](https://knulli.org/) on the Anbernic RG40XX devices.  This
leverages the LED Daemon from [chrizzo-hb](https://github.com/chrizzo-hb).

## Installation

Log into the device via ssh and execute the following command:

```bash
curl https://raw.githubusercontent.com/zarquon-42/knulli-led-per-game/refs/heads/main/install.sh | bash
```

## Development Notea

This uses the library `Pillow` and `numpy` which are already installed within
Knulli but you may need to create a virtual environment on your dev machine.
