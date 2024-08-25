### Disclaimer

This project is not endorsed by or affiliated with Overwolf, Home Assistant, or Psyonix.

# Rocket League ButtPlug

Connect your buttplug to your score in Rocket League.

## Installation

Download the latest release or clone the repo and run main.py with Poetry

### Requirements

- RLBP (obviously)
- Intiface Central
- Overwolf
- Overwolf app [Home Assistant Game Events](https://www.overwolf.com/app/BinaryBurger-HomeAssistant_Game_Events)

### Setup

1. Launch Intiface Central
2. Start the server and configure your devices
3. Launch RLBP and click the server address to copy it to your clipboard
4. Launch Overwolf and open the Home Assistant Game Events app
5. Paste the server address into Webhook URL, set Throttle to 1 and click on Save
6. Launch your game and enjoy! :3

## Potential improvements

- Better config system
- Code comments
- Use an actual json library
- Toggleable dark mode for the ui?
- Game launch detection
- Gamemode detection


## Acknowledgements

- Heavily inspired by [BPGE](https://github.com/allanf181/BPGE)
- Powered by [buttplug.io](https://buttplug.io) and [buttplug-py](https://github.com/Siege-Wizard/buttplug-py)

## License

[MIT](https://choosealicense.com/licenses/mit/)
