### Disclaimer

This project is not endorsed by or affiliated with Overwolf, Home Assistant, or Psyonix.

# Rocket League ButtPlug

Connect your buttplug to your score in Rocket League.

## Installation

Download the code run main.py with Poetry

### Requirements

- **RLBP** (obviously)
- **Intiface Central**
- **Overwolf**
- **[Home Assistant Game Events](https://www.overwolf.com/app/BinaryBurger-HomeAssistant_Game_Events)**

### Setup

1. Launch **Intiface Central**
2. Start the Intiface server and set up your devices
3. Launch **RLBP** and click the server address to copy it to your clipboard
4. Launch **Overwolf** and open the **Home Assistant Game Events** app
5. Paste the server address into Webhook URL, set Throttle to 1 and click Save
6. Launch Rocket League and enjoy! :3

## Troubleshooting

### Intiface Central

For setup/use: **[Quickstart Guide](https://docs.intiface.com/docs/intiface-central/quickstart)**

For device troubleshooting: **[Bluetooth Devices Guide](https://docs.intiface.com/docs/intiface-central/hardware/bluetooth)**

### RLBP

- **RLBP** can't connect to **Intiface Central**:
  - Ensure the Intiface server is running
  - Verify **RLBP** is using the correct IP address (Default is ```ws://127.0.0.1:12345```)

- **RLBP** can't find my device:
  - Check if the device is connected in Intiface Central

- **RLBP** not getting your score:
  - Check that **Home Assistant Game Events** is running
  - Make sure **Home Assistant Game Events** has the correct server address:
  - Click the top button in **RLBP** to copy the server address

## Potential improvements

- Better config system
- Code comments
- Use an actual json library
- Game launch detection
- Gamemode detection
- Make an icon

## Acknowledgements

- Heavily inspired by **[BPGE](https://github.com/allanf181/BPGE)**
- Powered by **[buttplug.io](https://buttplug.io)** and **[buttplug-py](https://github.com/Siege-Wizard/buttplug-py)**

## License

[MIT](https://choosealicense.com/licenses/mit/)
