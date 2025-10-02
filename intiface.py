# intiface.py

import asyncio
import logging
from logging import NullHandler

from buttplug import Client, Device, ProtocolSpec, WebsocketConnector
from PySide6 import QtWidgets

import server
from actuators import vibrate_all, vibrate_one
from config_lib import load_config
from config_window import ConfigEditorWindow

class IntifaceManager:
    def __init__(self, gui):
        self.gui = gui
        self.client = None
        self.connector = None

        self.previous_score_increase = None
        self.listening = False
        self.contact = False

    async def config(self):
        # Check for config file
        try:
            with open("config.yaml", "r"):
                print("Config.yaml file found")
                self.gui.print("Config.yaml file found")
        except FileNotFoundError:
            print("Config.yaml file not found")
            self.gui.print("Config.yaml file not found")

        try:
            config = load_config()
            self.intiface_ip = config["intiface_ip"]
            self.min_vibe_strength = config["min_vibe_strength"]
            self.max_vibe_strength = config["max_vibe_strength"]
            self.min_vibe_time = config["min_vibe_time"]
            self.max_vibe_time = config["max_vibe_time"]
            self.vibe_strength_divider = config["vibe_strength_divider"]
            self.vibe_time_divider = config["vibe_time_divider"]
            self.min_vibe_score = config["min_vibe_score"]
        except Exception as e:
            print(f"Failed to load config values: {e}")
            self.gui.print(f"Failed to load config values: {e}")
            return
        print("Config values loaded")
        self.gui.print("Config values loaded")

    def connect_connector(self):
        self.connector = WebsocketConnector(
            self.intiface_ip,
            logger=logging.getLogger().addHandler(NullHandler()),
        )

    async def create_client(self):
        self.client = Client(
            "RLBP",
            ProtocolSpec.v3,
        )
        self.connect_connector()

        try:
            await self.client.connect(self.connector)
        except:  # noqa: E722
            print("Unable to connect to Intiface")
            self.gui.print("Unable to connect to Intiface")
            return
        self.gui.print("Connected to Intiface")

    async def disconnect(self):
        if self.client and self.client.connected:
            await self.client.disconnect()
            print("Disconnecting from Intiface")

    async def reconnect(self):
        if self.client:
            if not self.client.connected:
                self.gui.print("Attempting to connect to Intiface")
            else:
                await self.client.disconnect()
                self.gui.print("Disconnected from Intiface")
            
            try:
                self.connect_connector() # Recreate connector after config reload
                await self.client.connect(self.connector)
                if self.client.connected:
                    self.gui.print("Connected to Intiface")
                else:
                    self.gui.print("Unable to connect to Intiface")
            except Exception as e:
                print(f"{e}")
                self.gui.print("Unable to connect to Intiface")

    async def test_all_devices(self):
        if self.client.connected:
            if self.client.devices:
                for device in self.client.devices.values():
                    await self.test_one_device(device)
            else:
                self.gui.print("No devices found, use Intiface to manage your devices")
        else:
            self.gui.print("Not connected to Intiface")

    async def test_one_device(self, device: Device):
        time = 1
        strength = 0.5

        self.gui.print(f"Testing {device.name}")
        if device.actuators:
            self.gui.print(f"{len(device.actuators)} generic actuator(s) found")
            self.gui.print("Activating for 1 second at 50% strength")
            self.gui.print(f"[{time = }] [{strength = }]")
            asyncio.create_task(vibrate_one(device, strength, time))
        elif device.linear_actuators:
            self.gui.print(
                f"{len(device.linear_actuators)} linear actuator(s) found, these are unsupported in RLBP"
            )
        elif device.rotatory_actuators:
            self.gui.print(
                f"{len(device.rotatory_actuators)} rotatory actuator(s) found, these are unsupported in RLBP"
            )
        else:
            self.gui.print("No actuators found, somehow. Try reconnecting your device")

    async def stop_vibrate(self):
        self.gui.print("Stopping current vibration")
        asyncio.create_task(vibrate_all(self, 0, 0))

    async def contact_status(self):
        while self.contact is False:
            self.server.first_contact(self)
            if self.contact is True:
                self.gui.print("Got something from Rocket League!")
                return
            asyncio.sleep(0.1)

    async def score_vibrate(self):
        if self.listening is True:
            self.listening = False
            self.gui.button4.setText("Start Score Monitoring")
            return
        else:
            self.listening = True
            self.gui.button4.setText("Stop Score Monitoring")

        self.gui.print("Started listening for score")
        while True:
            if self.listening is False:
                self.gui.print("Stopped listening for score")
                self.stop_vibrate()
                return

            score_increase = server.get_score_increase()
            if (
                score_increase is not None
                and score_increase != self.previous_score_increase
                and score_increase >= self.min_vibe_score
            ):
                self.gui.print("\n")
                self.gui.print(f"Score increased by {score_increase}")
                strength = score_increase / self.vibe_strength_divider
                time = score_increase / self.vibe_time_divider
                strength = max(
                    self.min_vibe_strength,
                    min(self.max_vibe_strength, strength),
                )
                time = max(self.min_vibe_time, min(self.max_vibe_time, time))
                if self.client.devices:
                    self.gui.print(f"Activating at {strength:.0f}% for {time:.1f} seconds")
                    # strength needs to be a float between 0.0 and 1.0
                    asyncio.create_task(vibrate_all(self, strength / 100, time))

            self.previous_score_increase = score_increase

            await asyncio.sleep(0.1)
    
    async def edit_config(self):
        config_window = ConfigEditorWindow(self.gui)
        result = config_window.exec()
        
        if result == QtWidgets.QDialog.Accepted:
            await self.config()