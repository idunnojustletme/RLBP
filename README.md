# Rocket League ButtPlug

Connect your buttplug to your score in Rocket League.

### Disclaimer

This project is not endorsed by or affiliated with Overwolf, Home Assistant, or Psyonix.

## Installation

### Using the EXE (recommended)

1. Download the latest release .zip file
2. Extract it
3. Run main.exe

### Running the code yourself (hard mode)

1. Clone this repository ```git clone https://github.com/idunnojustletme/RLBP```
2. Spin up a virtual environment in the same directory as the project (```python -m venv .venv```)
3. Activate the virtual environment

- Windows: ```.\.venv\Scripts\activate```
- Linux/MacOS: ```source .venv/bin/activate```

4. With the virtual environment active, install the dependencies with ```pip install -r requirements.txt```
5. Run main.py (```python main.py```)

### Requirements

- **RLBP** (obviously)
- **Intiface Central**
- **Overwolf**
- **[Home Assistant Game Events](https://www.overwolf.com/app/BinaryBurger-HomeAssistant_Game_Events)**

### Setup

Note: Overwolf is designed for Windows, so sorry to my Linux brethren. I did all I could.

1. Launch **Intiface Central**
2. Start the Intiface server and set up your devices
3. Launch **RLBP** and click the server address to copy it to your clipboard
4. Launch **Overwolf** and open the **Home Assistant Game Events** app
5. Paste the server address into Webhook URL, set Throttle to 1, and click Save
6. Launch Rocket League and enjoy! :3

7. Bonus step: Check out the config.yaml file that came with the EXE and adjust to your liking

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
- Use an actual JSON library
- Game launch detection
- Gamemode detection
- Make an icon

## Acknowledgements

- Heavily inspired by **[BPGE](https://github.com/allanf181/BPGE)**
- Powered by **[buttplug.io](https://buttplug.io)** and **[buttplug-py](https://github.com/Siege-Wizard/buttplug-py)**
